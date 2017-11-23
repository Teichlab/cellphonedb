import math

import pandas as pd

from tools.app import output_dir
from tools.interaction_actions import _only_uniprots_in_df


def _validate_sources(generated_sources, original_sources):
    '''
    Check if all original soruces exist in generated source
    :type generated_sources: list
    :type original_sources: list
    :rtype: bool
    '''

    generated_sources = list(set(generated_sources))
    original_sources = list(set(original_sources))
    not_existent_source = []
    for source in original_sources:
        if source not in generated_sources:
            not_existent_source.append(source)

    if not_existent_source:
        print('WARN: Some sources did exist in generated file')
        print(not_existent_source)
        return False

    return True


def generate_interactions_custom(interactions_base_df, protein_df, gene_df):
    '''

    :type interactions_base_df: pd.DataFrame()
    :typetype protein_df: pd.DataFrame()
    :type gene_df: pd.DataFrame()
    :rtype: pd.DataFrame()
    '''
    interactions_base_df.dropna(how='any', subset=['A', 'B'], inplace=True)

    custom_interactions = pd.DataFrame()

    custom_interactions['a_raw_data'] = interactions_base_df['A']
    custom_interactions['b_raw_data'] = interactions_base_df['B']
    custom_interactions['a_raw_ensembl'] = interactions_base_df['altA']
    custom_interactions['b_raw_ensembl'] = interactions_base_df['altB']

    def extract_uniprot(row_value):
        id_type = row_value['B'].split(':')[0]
        if id_type == 'uniprotkb':
            return row_value['B'].split(':')[1].split('-')[1]

        return pd.np.nan

    custom_interactions['protein_1'] = interactions_base_df[
        interactions_base_df['A'].apply(lambda value: value.split(':')[0] == 'uniprotkb')]['A'].apply(
        lambda value: value.split(':')[1].split('-')[0])

    custom_interactions['protein_2'] = interactions_base_df[
        interactions_base_df['B'].apply(lambda value: value.split(':')[0] == 'uniprotkb')]['B'].apply(
        lambda value: value.split(':')[1].split('-')[0])

    custom_interactions['source'] = interactions_base_df['provider']

    custom_interactions['raw_score'] = interactions_base_df['confidenceScore']  # .apply(extract_score)

    # Extract ensembl for a_raw_ensembl data. Only if value is not null and has ensembl: prefix
    custom_interactions['ensembl_1'] = custom_interactions.dropna(subset=['a_raw_ensembl'])[
        custom_interactions.dropna(subset=['a_raw_ensembl'])['a_raw_ensembl'].apply(
            lambda value: value.split(':')[0] == 'ensembl')][
        'a_raw_ensembl'].apply(
        lambda value: value.split(':')[1])

    custom_interactions['ensembl_2'] = custom_interactions.dropna(subset=['b_raw_ensembl'])[
        custom_interactions.dropna(subset=['b_raw_ensembl'])['b_raw_ensembl'].apply(
            lambda value: value.split(':')[0] == 'ensembl')][
        'b_raw_ensembl'].apply(
        lambda value: value.split(':')[1])

    custom_interactions = pd.merge(custom_interactions, gene_df, left_on='ensembl_1', right_on='ensembl', how='outer',
                                   indicator='_merge_1')

    custom_interactions.drop(['ensembl'], inplace=True, axis=1)
    custom_interactions = pd.merge(custom_interactions, gene_df, left_on='ensembl_2', right_on='ensembl', how='outer',
                                   indicator='_merge_2', suffixes=['_1', '_2'])

    def get_protein(row, protein_number):
        protein_x = row['protein_%s' % protein_number]
        if isinstance(protein_x, float) and math.isnan(protein_x):
            return row['uniprot_%s' % protein_number]

        return row['protein_%s' % protein_number]

    custom_interactions['protein_1'] = custom_interactions.apply(lambda row: get_protein(row, 1), axis=1)
    custom_interactions['protein_2'] = custom_interactions.apply(lambda row: get_protein(row, 2), axis=1)

    custom_interactions.dropna(how='any', subset=['protein_1', 'protein_2'], inplace=True)

    custom_interactions = custom_interactions[['protein_1', 'protein_2', 'raw_score', 'source']]
    custom_interactions = _only_uniprots_in_df(protein_df, custom_interactions)

    def get_score(raw_score):
        intact_miscore = raw_score.split('intact-miscore:')
        if len(intact_miscore) < 2:
            return 1
        return float(intact_miscore[1])

    custom_interactions['score_1'] = custom_interactions['raw_score'].apply(get_score)
    custom_interactions['score_2'] = custom_interactions['score_1']

    def set_score_duplicates(interaction):
        interaction['score_1'] = \
            custom_interactions[(custom_interactions['protein_1'] == interaction['protein_1']) & (
                custom_interactions['protein_2'] == interaction['protein_2'])]['score_1'].max()

        interaction['score_2'] = \
            custom_interactions[(custom_interactions['protein_1'] == interaction['protein_1']) & (
                custom_interactions['protein_2'] == interaction['protein_2'])]['score_2'].max()

        return interaction

    custom_interactions = custom_interactions.apply(set_score_duplicates, axis=1)
    custom_interactions.drop_duplicates(['protein_1', 'protein_2', 'score_1', 'score_2'], keep='first', inplace=True)

    custom_interactions = custom_interactions[['protein_1', 'protein_2', 'score_1', 'score_2', 'source']]
    custom_interactions.to_csv(
        '%s/cellphone_interactions_custom.csv' % output_dir, index=False)

    _validate_sources(custom_interactions['source'].tolist(), interactions_base_df['provider'].tolist())

    return custom_interactions
