import os
from typing import Optional, Union, IO

import click
import pandas as pd

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import output_dir, data_dir
from cellphonedb.tools.actions import gene_actions
from cellphonedb.tools.generate_data.filters.non_complex_interactions import only_noncomplex_interactions
from cellphonedb.tools.generate_data.filters.remove_interactions import remove_interactions_in_file
from cellphonedb.tools.generate_data.getters import get_iuphar_guidetopharmacology
from cellphonedb.tools.generate_data.mergers.add_curated import add_curated
from cellphonedb.tools.generate_data.mergers.merge_interactions import merge_iuphar_imex_interactions
from cellphonedb.tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from cellphonedb.tools.generate_data.parsers.parse_interactions_imex import parse_interactions_imex
from cellphonedb.utils import utils
from cellphonedb.utils.utils import _get_separator


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


@click.command()
@click.option('--user-protein', type=click.File('r'), default=None)
@click.option('--fetch-uniprot', is_flag=True)
@click.option('--result-path', type=str, default=None)
@click.option('--log-file', type=str, default='log.txt')
def generate_proteins(user_protein: Optional[click.File],
                      fetch_uniprot: bool,
                      result_path: str,
                      log_file: str):
    # additional data comes from given file or uniprot remote url
    if fetch_uniprot:
        source_url = 'https://www.uniprot.org/uniprot/?query=*&format=tab&force=true' \
                     '&columns=id,entry%20name,reviewed,protein%20names,genes,organism,length' \
                     '&fil=organism:%22Homo%20sapiens%20(Human)%20[9606]%22%20AND%20reviewed:yes' \
                     '&compress=yes'

        additional_df = pd.read_csv(source_url, sep='\t', compression='gzip')
        print('read remote uniprot file')
    else:
        additional_df = pd.read_csv(os.path.join(data_dir, 'sources/uniprot.tab'), sep='\t')
        print('read remote uniprot file')

    curated_df: pd.DataFrame = pd.read_csv(os.path.join(data_dir, 'sources/protein_curated.csv'))

    output_path = _set_paths(output_dir, result_path)
    log_path = '{}/{}'.format(output_path, log_file)
    result = merge_proteins(curated_df, additional_df, log_path)

    if user_protein:
        separator = _get_separator(os.path.splitext(user_protein.name)[-1])
        user_df: pd.DataFrame = pd.read_csv(user_protein, sep=separator)

        result = merge_proteins(user_df, result, log_path)

    result.to_csv('{}/{}'.format(output_path, 'protein.csv'), index=False)


def merge_proteins(curated_df,
                   additional_df: pd.DataFrame,
                   log_file: str) -> pd.DataFrame:
    additional_df = additional_df.copy()

    defaults = {
        'receptor': False,
        'integrin_interaction': False,
        'other': False,
        'other_desc': None,
        'peripheral': False,
        'receptor_desc': None,
        'secreted_desc': None,
        'secreted_highlight': False,
        'secretion': False,
        'transmembrane': False,
        'pdb_structure': False,
        'pdb_id': None,
        'stoichiometry': None,
        'comments_complex': None,
        'adhesion': False,
        'tags': 'To_add',
        'tags_reason': None,
        'tags_description': None
    }
    used_cols = ['uniprot', 'entry_name'] + list(defaults.keys())

    # homogeneized column names
    additional_df.rename(index=str, columns={'Entry': 'uniprot', 'Entry name': 'entry_name'}, inplace=True)

    # # Here we set defaults for uniprot & curated data
    set_defaults(curated_df, defaults)
    set_defaults(additional_df, defaults)

    # we will only use these columns
    additional_df: pd.DataFrame = additional_df[used_cols]
    curated_df: pd.DataFrame = curated_df[used_cols]

    # type casting to ensure they are equal
    for column in additional_df:
        if additional_df[column].dtype == curated_df[column].dtype:
            continue

        print(f'converting `{column}` type from `{additional_df[column].dtype}` to `{curated_df[column].dtype}`')
        additional_df[column] = additional_df[column].astype(curated_df[column].dtype)

    additional_is_in_curated = additional_df['uniprot'].isin(curated_df['uniprot'])
    curated_is_in_additional = curated_df['uniprot'].isin(additional_df['uniprot'])

    common_additional: pd.DataFrame = additional_df.reindex(used_cols, axis=1)[additional_is_in_curated]
    common_curated = curated_df.reindex(used_cols, axis=1)[curated_is_in_additional]

    common_additional = common_additional.sort_values(by='uniprot')
    common_curated = common_curated.sort_values(by='uniprot')

    distinct_uniprots = additional_df[~additional_is_in_curated]
    result: pd.DataFrame = pd.concat([common_curated, distinct_uniprots], ignore_index=True, sort=True)

    common_curated['file'] = 'curated'
    common_additional['file'] = 'additional'

    merged = common_curated.append(common_additional).sort_values(by=used_cols)
    merged.to_csv(log_file, index=False, sep='\t')

    return result


def set_defaults(df, defaults):
    for column_name, default_value in defaults.items():
        if column_name not in df:
            print('missing column in dataframe: {}, set to default {}'.format(column_name, default_value))
            df[column_name] = default_value
            continue

        df[column_name].replace({pd.np.nan: default_value}, inplace=True)


def _set_paths(output_path, subfolder):
    if not output_path:
        output_path = output_dir

    if subfolder:
        output_path = os.path.realpath(os.path.expanduser('{}/{}'.format(output_path, subfolder)))

    os.makedirs(output_path, exist_ok=True)

    if _path_is_not_empty(output_path):
        app_logger.warning(
            'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))

    return output_path


def _path_is_not_empty(path):
    return bool([f for f in os.listdir(path) if not f.startswith('.')])
