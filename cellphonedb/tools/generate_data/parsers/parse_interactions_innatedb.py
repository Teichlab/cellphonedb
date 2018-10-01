import pandas as pd

from cellphonedb.src.core.utils.filters import remove_not_defined_columns
from tools.app import data_dir, output_dir
from tools.interactions_helper import _only_genes_in_df


def generate_interactions_innatedb(interactions_base_namefile, database_gene_namefile):
    interactions_base_df = pd.read_csv('%s/%s' % (data_dir, interactions_base_namefile), sep='\t', na_values='-')

    innatedb_inteactions = pd.DataFrame()

    innatedb_inteactions['gene_1'] = interactions_base_df['alt_identifier_A'].apply(
        lambda preformat_uniprot: preformat_uniprot.split(':')[1])
    innatedb_inteactions['gene_2'] = interactions_base_df['alt_identifier_B'].apply(
        lambda preformat_uniprot: preformat_uniprot.split(':')[1])

    innatedb_inteactions['score_1'] = 0
    innatedb_inteactions['score_2'] = 1

    innatedb_inteactions['source'] = 'innatedb'

    database_genes_df = pd.read_csv('%s%s' % (data_dir, database_gene_namefile))

    cellphone_interactions = _only_genes_in_df(database_genes_df, innatedb_inteactions)

    cellphone_interactions.rename(index=str, columns={'uniprot_1': 'protein_1', 'uniprot_2': 'protein_2'}, inplace=True)

    cellphone_interactions = remove_not_defined_columns(cellphone_interactions,
                                                        ['protein_1', 'protein_2', 'score_1', 'score_2', 'source'])

    cellphone_interactions.drop_duplicates(inplace=True)

    cellphone_interactions.to_csv('%s/cellphone_interactions_innatedb.csv' % output_dir, index=False)
