import os
from io import StringIO

import pandas as pd
import requests
import tqdm

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import data_dir


def read_imex_data(genes: pd.DataFrame, downloads_path: str, fetch: bool) -> pd.DataFrame:
    proteins = genes['uniprot'].tolist()

    sources = [
        {
            'name': 'InnateDB',
            'base_url': 'https://psicquic.curated.innatedb.com/webservices/current/search/query/species:human',
            'query_parameters': False,
        },
        {
            'name': 'InnateDB-All',
            'base_url': 'https://psicquic.all.innatedb.com/webservices/current/search/query/species:human',
            'query_parameters': False,
        },
        {
            'name': 'IMEx',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/imex/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'IntAct',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/intact/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'bhf-ucl',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/bhf-ucl/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'MatrixDB',
            'base_url': 'http://matrixdb.univ-lyon1.fr:8080/psicquic/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'MINT',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/mint/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'I2D',
            'base_url': 'http://ophid.utoronto.ca/psicquic-ws/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'UniProt',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/uniprot/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        {
            'name': 'MBInfo',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/mbinfo/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        # 'DIP': 'http://imex.mbi.ucla.edu/xpsq-dip-all/service/rest/current/search/query/{}',
    ]

    significant_columns = ['A', 'B', 'altA', 'altB', 'provider']
    carry = pd.DataFrame(columns=significant_columns)

    for source in tqdm.tqdm(sources, desc='Fetching sources'.ljust(20)):
        carry = carry.append(_get_source(source, proteins, downloads_path, significant_columns, fetch),
                             ignore_index=True,
                             sort=False)
    print()

    carry.drop_duplicates(inplace=True)
    print(carry)

    return carry


def _get_source(source, proteins, downloads_path, significant_columns, fetch: bool, save_backup: bool = True):
    carry = pd.DataFrame(columns=significant_columns)
    columns_to_save = ['A', 'B', 'altA', 'altB']
    compression = 'gzip'
    download_file_path = os.path.join(downloads_path, '{}_interaction_raw.csv.gz'.format(source))

    def best_path_for(source: str):
        saved_file_path = os.path.join(data_dir, 'sources', '{}_interaction_raw.csv.gz'.format(source))

        if os.path.exists(download_file_path):
            return download_file_path
        if os.path.exists(saved_file_path):
            return saved_file_path

        app_logger.error('Could not find local source for {}'.format(source))
        exit(1)

    file_path = best_path_for(source['name'])

    try:
        if fetch:
            if source['query_parameters']:
                carry = _get_chunked_api_results(carry, columns_to_save, proteins, source)
            else:
                carry = _get_single_api_results(carry, columns_to_save, source)
        else:
            app_logger.warning('Using local version for source {}, using available backup'.format(source['name']))
            carry = pd.read_csv(file_path, compression=compression)

    except CouldNotFetchFromApiException:
        app_logger.warning('Could not fetch remote source {}, using available backup'.format(source['name']))
        carry = pd.read_csv(file_path, compression=compression)

    carry['provider'] = source['name']
    carry.drop_duplicates(inplace=True)

    if save_backup:
        carry.to_csv(download_file_path, index=False, compression=compression)

    return carry


class CouldNotFetchFromApiException(Exception):
    pass


def _get_chunked_api_results(carry, columns_to_save, proteins, source):
    chunk_size = 10
    for idx, chunk in tqdm.tqdm(enumerate(zip(*[iter(proteins)] * chunk_size)),
                                desc=source['name'].ljust(20),
                                total=int(len(proteins) / chunk_size)):
        url = source['base_url'].format(' or '.join(chunk))
        try:
            response = requests.get(url)

            if response.text:
                s = StringIO(response.text)
                df = pd.read_csv(s, sep='\t', names=columns_to_save, usecols=range(4), na_values='-')
                carry = pd.concat([carry, df], sort=False, axis=0, ignore_index=True)
                carry.drop_duplicates(inplace=True)
            else:
                if response.status_code != 200:
                    raise CouldNotFetchFromApiException()
        except requests.ConnectionError:
            raise CouldNotFetchFromApiException()

    return carry


def _get_single_api_results(carry, columns_to_save, source):
    url = source['base_url']
    response = requests.get(url)
    try:
        if response.text:
            s = StringIO(response.text)
            df = pd.read_csv(s, sep='\t', names=columns_to_save, usecols=range(4), na_values='-')
            carry = pd.concat([carry, df], sort=False, axis=0, ignore_index=True)
            carry.drop_duplicates(inplace=True)

        else:
            if response.status_code != 200:
                raise CouldNotFetchFromApiException()

    except requests.ConnectionError:
        raise CouldNotFetchFromApiException()

    return carry
