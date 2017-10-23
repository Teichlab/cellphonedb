import os

import pandas as pd

from tools.app import current_dir
from cellcommdb.tools import filters


def merge_gene_mouse(gene_human, gene_mouse):
    """
    Loads gene table from csv.
    - Load human gene data
    - Complete human table gene data with mouse data
    :param gene_file:
    :return:
    """

    gene_file = os.path.join(current_dir, 'data', gene_human)
    csv_gene_df = pd.read_csv(gene_file)

    # Complete with gene mouse data
    gene_mouse_csv_file = os.path.join(current_dir, 'data', gene_mouse)
    csv_gene_mouse = pd.read_csv(gene_mouse_csv_file)

    gene_mouse_df = pd.merge(csv_gene_df, csv_gene_mouse, left_on=['ensembl', 'protein_uniprot'],
                             right_on=['human_ensembl', 'human_uniprot'], indicator=True, how='outer')

    if len(gene_mouse_df[gene_mouse_df['_merge'] == 'right_only']):
        print('SOME MOUSE GENE DIDNT EXIST IN HUMAN GENE')
        print(gene_mouse_df[gene_mouse_df['_merge'] == 'right_only'][['human_ensembl', 'human_uniprot']])

    gene_mouse_df = gene_mouse_df[(gene_mouse_df['_merge'] == 'left_only') | (gene_mouse_df['_merge'] == 'both')]

    gene_mouse_df.rename(index=str, columns={'human_ensembl': 'ensembl'}, inplace=True)
    gene_mouse_df.rename(index=str, columns={'protein_uniprot': 'name'}, inplace=True)
    filters.remove_not_defined_columns(gene_mouse_df,
                                       ['ensembl', 'gene_name', 'mouse_uniprot', 'mouse_ensembl', 'name'])

    output_name = _filename_parameter(gene_human, 'merged')
    gene_mouse_df.to_csv('%s/out/%s' % (current_dir, output_name), index=False)


def _filename_parameter(protein_file, parameter):
    splited_filename = protein_file.split('.')
    splited_filename[-2] = '%s_%s' % (splited_filename[-2], parameter)
    output_name = '.'.join(splited_filename)
    return output_name
