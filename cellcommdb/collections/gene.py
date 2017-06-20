import os

import pandas as pd
from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Gene, Protein, Multidata
from cellcommdb.tools import filters, database


def load(gene_file=None):
    if not gene_file:
        gene_file = os.path.join(current_dir, 'data', 'gene_table.csv')

    protein_query = db.session.query(Protein)
    protein_df = pd.read_sql(protein_query.statement, db.engine)

    multidata_query = db.session.query(Multidata)
    multidata_df = pd.read_sql(multidata_query.statement, db.engine)

    multidata_df.rename(index=str, columns={'id': 'multidata_id'}, inplace=True)
    protein_multidata_df = pd.merge(protein_df, multidata_df, left_on='protein_multidata_id', right_on='multidata_id')

    csv_gene_df = pd.read_csv(gene_file, quotechar='"')

    protein_multidata_df.rename(index=str, columns={'name': 'uniprot'}, inplace=True)
    gene_df = pd.merge(csv_gene_df, protein_multidata_df, left_on='protein_uniprot', right_on='uniprot')
    gene_df.rename(index=str, columns={'id': 'protein_id'}, inplace=True)

    if len(csv_gene_df) > len(gene_df):
        csv_prots = csv_gene_df['protein_uniprot'].tolist()
        result_prots = gene_df['protein_uniprot'].tolist()

        missing_prots = []
        for csv_prot in csv_prots:
            if csv_prot not in result_prots:
                missing_prots.append(csv_prot)

        print 'SOME PROTEINS DIDNT EXIST'
        missing_prots = list(set(missing_prots))
        for missing_prot in missing_prots:
            print missing_prot

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
