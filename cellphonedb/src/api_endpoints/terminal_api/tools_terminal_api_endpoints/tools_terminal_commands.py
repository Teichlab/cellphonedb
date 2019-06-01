import io
import os
import zipfile
from typing import Union

import click
import pandas as pd
import requests

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import output_dir
from cellphonedb.tools.actions import gene_actions
from cellphonedb.tools.generate_data.filters.non_complex_interactions import only_noncomplex_interactions
from cellphonedb.tools.generate_data.filters.remove_interactions import remove_interactions_in_file
from cellphonedb.tools.generate_data.getters import get_iuphar_guidetopharmacology
from cellphonedb.tools.generate_data.mergers.add_curated import add_curated
from cellphonedb.tools.generate_data.mergers.merge_interactions import merge_iuphar_imex_interactions
from cellphonedb.tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from cellphonedb.tools.generate_data.parsers.parse_interactions_imex import parse_interactions_imex
from cellphonedb.utils import utils


# TODO: move to separate modules
@click.command()
@click.option('--version', type=str, default='latest')
def download_database(version: str):
    try:
        if not version or version == 'latest':
            latest_release = _latest_release()

            version = latest_release['tag']
            zip_to_download = latest_release['url']
        else:
            releases = _list_releases()

            if version not in releases:
                app_logger.error('Unavailable version selected')
                app_logger.error('Available versions are: {}'.format(', '.join(releases.keys())))
                exit(1)

            zip_to_download = releases[version]['url']

        print('Downloading {} release of database'.format(version))

        output_folder = os.path.expanduser('~/.cpdb/releases/{}'.format(version))
        os.makedirs(output_folder, exist_ok=True)

        zip_response = requests.get(zip_to_download)
        with zipfile.ZipFile(io.BytesIO(zip_response.content)) as thezip:
            root_folder = thezip.namelist()[0]
            for name in thezip.namelist():
                if name.endswith('/'):
                    continue

                file_folder = os.path.dirname(name)
                file_name = os.path.basename(name)

                dest_folder = os.path.realpath(os.path.join(output_folder, os.path.relpath(file_folder, root_folder)))
                dest_file = os.path.join(dest_folder, file_name)
                os.makedirs(dest_folder, exist_ok=True)
                with thezip.open(name) as zf:
                    with open(dest_file, 'wb') as fw:
                        fw.write(zf.read())

    except NoReleasesException:
        print('There are no versions available (or connection could not be made to server to retrieve them)')
        exit(1)


@click.command()
def list_versions():
    try:
        releases: dict = _list_releases()

        for idx, (_, version) in enumerate(releases.items()):
            note = ' *latest' if idx == 0 else ''
            print('version {}{}: released: {}, url: {}'.format(version['tag'], note, version['date'], version['link']))

    except NoReleasesException:
        print('There are no versions available (or connection could not be made to server to retrieve them)')
        exit(1)


class NoReleasesException(Exception):
    pass


def _list_releases():
    try:
        releases = _github_query('releases')

        if not releases:
            raise NoReleasesException()

        return _format_releases(*releases)

    except requests.exceptions.ConnectionError:
        raise NoReleasesException()


def _latest_release():
    try:
        latest_release = _github_query('latest')

        if not latest_release:
            raise NoReleasesException()

        return _format_release(latest_release)

    except requests.exceptions.ConnectionError:
        raise NoReleasesException()


def _github_query(kind) -> Union[dict, list]:
    queries = {
        'releases': 'https://api.github.com/repos/{}/{}/releases'.format('ydevs', 'cpdb-data'),
        'latest': 'https://api.github.com/repos/{}/{}/releases/latest'.format('ydevs', 'cpdb-data')
    }

    query = queries[kind]

    response = requests.get(query, headers={'Accept': 'application/vnd.github.v3+json'})

    if response.status_code != 200:
        raise NoReleasesException()

    return response.json()


def _format_releases(*releases) -> dict:
    return {item['tag_name']: _format_release(item) for item in releases}


def _format_release(item) -> dict:
    return {'url': item['zipball_url'],
            'tag': item['tag_name'],
            'date': item['published_at'],
            'link': item['html_url']}


@click.command()
@click.argument('uniprot_db_filename')
@click.argument('ensembl_db_filename')
@click.argument('proteins_filename')
@click.argument('remove_genes_filename')
@click.argument('hla_genes_filename')
@click.option('--result_filename', default='gene.csv')
@click.option('--result_path', default='')
@click.option('--gene_uniprot_ensembl_merged_result_filename', default='gene_uniprot_ensembl_merged.csv')
@click.option('--add_hla_result_filename', default='gene_hla_added.csv')
def generate_genes(
        uniprot_db_filename: str,
        ensembl_db_filename: str,
        proteins_filename: str,
        remove_genes_filename: str,
        hla_genes_filename: str,
        result_filename: str,
        result_path: str,
        gene_uniprot_ensembl_merged_result_filename: str,
        add_hla_result_filename: str) -> None:

    output_path = _set_paths(output_dir, result_path)

    def prefix_output_path(filename: str) -> str:
        return '{}/{}'.format(output_path, filename)

    gene_actions.generate_genes_from_uniprot_ensembl_db(uniprot_db_filename,
                                                        ensembl_db_filename,
                                                        proteins_filename,
                                                        prefix_output_path(gene_uniprot_ensembl_merged_result_filename)
                                                        )

    gene_actions.add_hla_genes(prefix_output_path(gene_uniprot_ensembl_merged_result_filename),
                               hla_genes_filename,
                               prefix_output_path(add_hla_result_filename),
                               )

    gene_actions.remove_genes_in_file(prefix_output_path(add_hla_result_filename),
                                      remove_genes_filename,
                                      prefix_output_path(result_filename),
                                      )

    gene_actions.validate_gene_list(prefix_output_path(result_filename))


@click.command()
@click.argument('imex_raw_filename')
@click.argument('iuphar_raw_filename')
@click.argument('database_proteins_filename', default='protein.csv')
@click.argument('database_gene_filename', default='gene.csv')
@click.argument('database_complex_filename', default='complex.csv')
@click.argument('interaction_to_remove_filename')
@click.argument('interaction_curated_filename')
@click.option('--result_path', default='')
def generate_interactions(
        imex_raw_filename: str,
        iuphar_raw_filename: str,
        database_proteins_filename: str,
        database_gene_filename: str,
        database_complex_filename: str,
        interaction_to_remove_filename: str,
        interaction_curated_filename: str,
        result_path: str,
) -> None:
    interactions_base = utils.read_data_table_from_file(imex_raw_filename, na_values='-')
    proteins = pd.read_csv(database_proteins_filename)
    genes = pd.read_csv(database_gene_filename)
    complexes = pd.read_csv(database_complex_filename)
    interactions_to_remove = pd.read_csv(interaction_to_remove_filename)
    interaction_curated = pd.read_csv(interaction_curated_filename)

    print('generating imex file')
    imex_interactions = parse_interactions_imex(interactions_base, proteins, genes)

    output_path = _set_paths(output_dir, result_path)
    download_path = _set_paths(output_path, 'downloads')

    print('Getting Iuphar interactions')
    iuphar_original = get_iuphar_guidetopharmacology.call(iuphar_raw_filename,
                                                          download_path,
                                                          default_download_response='no',
                                                          )

    print('generating iuphar file')
    iuphar_interactions = parse_iuphar_guidetopharmacology.call(iuphar_original, genes, proteins)

    print('merging iuphar/imex')
    merged_interactions = merge_iuphar_imex_interactions(iuphar_interactions, imex_interactions)

    print('removing complex interactions')
    no_complex_interactions = only_noncomplex_interactions(merged_interactions, complexes)

    print('removing selected interactions')
    clean_interactions = remove_interactions_in_file(no_complex_interactions, interactions_to_remove)

    print('adding curated interaction')
    interactions_with_curated = add_curated(clean_interactions, interaction_curated)

    interactions_with_curated.to_csv('{}/interaction.csv'.format(output_path), index=False)


def _set_paths(output_path, project_name):
    if not output_path:
        output_path = output_dir

    if project_name:
        output_path = os.path.realpath(os.path.expanduser('{}/{}'.format(output_path, project_name)))

    os.makedirs(output_path, exist_ok=True)

    if _path_is_not_empty(output_path):
        app_logger.warning(
            'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))

    return output_path


def _path_is_not_empty(path):
    return bool([f for f in os.listdir(path) if not f.startswith('.')])
