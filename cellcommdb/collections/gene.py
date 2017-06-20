import os

import pandas as pd
from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Gene, Protein, Multidata
from cellcommdb.tools import filters, database


def load(gene_file=None):
    if not gene_file:
        gene_file = os.path.join(current_dir, 'data', 'gene_table.csv')


    protein_query = db.session.query(Protein.id, Multidata.name).join(Multidata)
    protein_multidata_df = pd.read_sql(protein_query.statement, db.engine)

    csv_gene_df = pd.read_csv(gene_file, quotechar='"')

    protein_multidata_df.rename(index=str, columns={'name': 'uniprot'}, inplace=True)
    gene_df = pd.merge(protein_multidata_df, csv_gene_df, left_on='uniprot', right_on='protein_uniprot', indicator=True, how='outer')
    gene_df.rename(index=str, columns={'id': 'protein_id'}, inplace=True)

    if len(gene_df[gene_df['_merge'] == 'right_only']):
        print 'SOME PROTEINS DIDNT EXIST'
        print gene_df[gene_df['_merge'] == 'right_only'].drop_duplicates('protein_uniprot')

    gene_df = gene_df[gene_df['_merge'] == 'both']
    gene_df.drop('_merge', axis=1, inplace=True)


    # Load gene_mouse
    gene_mouse_csv_file = os.path.join(current_dir, 'data', 'HumanMouseEnsembl_RVT.csv')

    csv_gene_mouse = pd.read_csv(gene_mouse_csv_file)

    gene_mouse_df = pd.merge(gene_df, csv_gene_mouse, left_on=['ensembl', 'uniprot'],
                             right_on=['human_ENSEMBL', 'human_uniprot'], indicator=True, how='outer')
    gene_mouse_df.rename(index=str, columns={'mouse_ENSEMBL': 'mouse_ensembl'}, inplace=True)

    if len(gene_mouse_df[gene_mouse_df['_merge'] == 'right_only']):
        print 'SOME GENE DIDNT EXIST'
        print gene_mouse_df[gene_mouse_df['_merge'] == 'right_only']

    gene_mouse_df = gene_mouse_df[(gene_mouse_df['_merge'] == 'left_only') | (gene_mouse_df['_merge'] == 'both')]

    filters.remove_not_defined_columns(gene_mouse_df, database.get_column_table_names(Gene, db))

    gene_mouse_df.to_sql(name='gene', if_exists='append', con=db.engine, index=False)
