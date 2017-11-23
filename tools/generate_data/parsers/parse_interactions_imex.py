import math

import pandas as pd

from tools.app import data_dir, output_dir
from tools.interaction_actions import _only_uniprots_in_df


def generate_interactions_imex(interactions_base_namefile, database_proteins_namefile):
    interactions_base_df = pd.read_csv('%s/%s' % (data_dir, interactions_base_namefile), sep='\t', na_values='-')

    interactions_base_df.dropna(how='any', subset=['A', 'B'], inplace=True)

    interactions_base_df['confidenceScore'].replace('nan', pd.np.NaN, inplace=True)

    imex_inteactions = pd.DataFrame()

    imex_inteactions['protein_1'] = interactions_base_df['A'].apply(
        lambda preformat_uniprot: preformat_uniprot.split(':')[1].split('-')[0])
    imex_inteactions['protein_2'] = interactions_base_df['B'].apply(
        lambda preformat_uniprot: preformat_uniprot.split(':')[1].split('-')[0])

    def extract_score(row):
        if isinstance(row, float) and math.isnan(row):
            return 0
        return row.split('intact-miscore:')[1]

    imex_inteactions['score_1'] = interactions_base_df['confidenceScore'].apply(extract_score)

    imex_inteactions['score_2'] = imex_inteactions['score_1']

    imex_inteactions['source'] = interactions_base_df['provider']

    database_proteins_df = pd.read_csv('%s/%s' % (data_dir, database_proteins_namefile))

    cellphone_interactions = _only_uniprots_in_df(database_proteins_df, imex_inteactions)

    def set_score_duplicates(interaction):
        interaction['score_1'] = \
            cellphone_interactions[(cellphone_interactions['protein_1'] == interaction['protein_1']) & (
                cellphone_interactions['protein_2'] == interaction['protein_2'])]['score_1'].max()

        interaction['score_2'] = \
            cellphone_interactions[(cellphone_interactions['protein_1'] == interaction['protein_1']) & (
                cellphone_interactions['protein_2'] == interaction['protein_2'])]['score_2'].max()

        return interaction

    interactions = cellphone_interactions.apply(set_score_duplicates, axis=1)

    interactions.drop_duplicates(keep='first', inplace=True)

    interactions.to_csv('%s/cellphone_interactions_imex.csv' % output_dir, index=False)
