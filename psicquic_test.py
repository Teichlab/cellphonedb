#!/usr/bin/env python3
import sys
from io import StringIO

import pandas as pd
import requests
import tqdm as tqdm

proteins = pd.read_csv(sys.argv[1])['uniprot'].tolist()

sources = \
    [
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
            'name': ' MINT',
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
            'name': ' MBInfo',
            'base_url': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/mbinfo/webservices/current/search/query/{}',
            'query_parameters': True,
        },
        # 'DIP': 'http://imex.mbi.ucla.edu/xpsq-dip-all/service/rest/current/search/query/{}',

    ]

# Create interaction_imex_raw.csv with all sources


for source in sources:
    print('\n')
    print(source['name'])
    carry = pd.DataFrame()
    if source['query_parameters']:
        for idx, chunk in tqdm.tqdm(enumerate(zip(*[iter(proteins)] * 500))):
            url = source['base_url'].format('{}'.format(' or '.join(chunk)))
            print(url)
            response = requests.get(url)

            if response.text:
                s = StringIO(response.text)
                df = pd.read_csv(s, sep='\t', header=None)
                carry = pd.concat([carry, df], sort=False, axis=0)
                carry.drop_duplicates(inplace=True)
            else:
                print(url)
                print('{} it {} is empty. Status code: {}'.format(source['name'], idx, response.status_code))

    else:
        url = source['base_url']
        response = requests.get(url)

        if response.text:
            s = StringIO(response.text)
            df = pd.read_csv(s, sep='\t', names=['A', 'B', 'altA', 'altB'], usecols=range(4))
            print(df)
            carry = pd.concat([carry, df], sort=False, axis=0)
            carry.drop_duplicates(inplace=True)
        else:
            print(url)
            print('{} is empty. Status code: {}'.format(source['name'], response.status_code))

    carry['provider'] = source['name']
    carry.to_csv('out/psicquic/{}_interaction_raw.csv'.format(source['name']), index=False)

carry = pd.DataFrame(columns=['A', 'B', 'altA', 'altB', 'provider'])

for source in sources:
    print(source['name'])
    source_data = pd.read_csv('out/psicquic/{}_interaction_raw.csv'.format(source['name']))
    source_data.rename(columns={'0': 'A', '1': 'B', '2': 'altA', '3': 'altB'}, index=str, inplace=True)
    carry = carry.append(source_data[['A', 'B', 'altA', 'altB', 'provider']], sort=False, ignore_index=True)

carry.to_csv('out/IMEX_all_sources.csv', index=False)
