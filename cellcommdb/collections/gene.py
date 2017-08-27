import os

import pandas as pd
from cellcommdb.api import current_dir
from cellcommdb.blend import Blend
from cellcommdb.extensions import db
from cellcommdb.models import Gene, Protein, Multidata
from cellcommdb.tools import filters, database


def _load_human(gene_file=None):
    """
    Load human gene data
    :param gene_file:
    :return:
    """
    if not gene_file:
        gene_file = os.path.join(current_dir, 'data', 'gene_table.csv')

    csv_gene_df = pd.read_csv(gene_file)

    gene_df = Blend.blend_protein(csv_gene_df, ['protein_uniprot'])

    return gene_df


def load(gene_file=None):
    """
    Loads gene table from csv.
    - Load human gene data
    - Complete human table gene data with mouse data
    :param gene_file:
    :return:
    """
    gene_df = _load_human(gene_file)

    # Complete with gene mouse data
    gene_mouse_csv_file = os.path.join(current_dir, 'data', 'HumanMouseEnsembl_RVT.csv')

    csv_gene_mouse = pd.read_csv(gene_mouse_csv_file)

    gene_mouse_df = pd.merge(gene_df, csv_gene_mouse, left_on=['ensembl', 'name'],
                             right_on=['human_ENSEMBL', 'human_uniprot'], indicator=True, how='outer')
    gene_mouse_df.rename(index=str, columns={'mouse_ENSEMBL': 'mouse_ensembl'}, inplace=True)

    if len(gene_mouse_df[gene_mouse_df['_merge'] == 'right_only']):
        print('SOME GENE DIDNT EXIST')
        print(gene_mouse_df[gene_mouse_df['_merge'] == 'right_only'][['human_ENSEMBL', 'human_uniprot']])

    gene_mouse_df = gene_mouse_df[(gene_mouse_df['_merge'] == 'left_only') | (gene_mouse_df['_merge'] == 'both')]

    filters.remove_not_defined_columns(gene_mouse_df, database.get_column_table_names(Gene, db))

    gene_mouse_df.to_sql(name='gene', if_exists='append', con=db.engine, index=False)
