import pandas as pd

from tools.tools_helper import interaction_exist, normalize_interactions


def merge_interactions(interactions_1, interactions_2, interaction_1_key='protein_1', interaction_2_key='protein_2'):
    """
    Merges two interactions dataframens prioritizing keeping first on duplicates
    """

    interactions_2_not_in_1 = interactions_2[
        interactions_2.apply(lambda row: interaction_exist(row, interactions_1, interaction_1_key, interaction_2_key),
                             axis=1) == False]

    interactions = interactions_1.append(interactions_2_not_in_1, sort=True)

    return interactions


def merge_iuphar_imex_interactions(iuphar_interactions: pd.DataFrame,
                                   imex_interactions: pd.DataFrame) -> pd.DataFrame():
    merge_result = merge_interactions(iuphar_interactions, imex_interactions, 'uniprot_1', 'uniprot_2')
    merge_result.fillna({'iuphar': False}, inplace=True)
    return merge_result


def merge_iuphar_other_and_curated_interactions(iuphar_other_interactions: pd.DataFrame,
                                                curated_interactions: pd.DataFrame) -> pd.DataFrame:
    all_interactions = iuphar_other_interactions.append(curated_interactions)

    all_interactions.reset_index(inplace=True, drop=True)
    normalized_interactions = normalize_interactions(all_interactions, 'multidata_name_1', 'multidata_name_2')

    duplicated_interactions = normalized_interactions[
        normalized_interactions.duplicated(['multidata_name_1', 'multidata_name_2'], keep=False)]

    unique_interactions = duplicated_interactions.drop_duplicates(['multidata_name_1', 'multidata_name_2'])

    def merge_values(interaction: pd.Series) -> pd.Series:
        interaction = interaction.copy()
        duplicated = duplicated_interactions[
            (duplicated_interactions['multidata_name_1'] == interaction['multidata_name_1']) & (
                    duplicated_interactions['multidata_name_2'] == interaction['multidata_name_2'])]

        if not duplicated[duplicated['source'] == 'curated'].empty:
            interaction = duplicated[duplicated['source'] == 'curated'].iloc[0]

        if duplicated['iuphar'].any():
            interaction['iuphar'] = True

        return interaction

    merged_duplicated_interactions = unique_interactions.apply(merge_values, axis=1)

    non_repeated_interactions = normalized_interactions.drop_duplicates(['multidata_name_1', 'multidata_name_2'],
                                                                        keep=False)
    interactions_merged = non_repeated_interactions.append(merged_duplicated_interactions, sort=True, ignore_index=True)
    interactions_merged.fillna({'iuphar': False}, inplace=True)
    interactions_merged = interactions_merged.astype(
        {'dlrp': bool, 'iuphar': bool})

    return interactions_merged
