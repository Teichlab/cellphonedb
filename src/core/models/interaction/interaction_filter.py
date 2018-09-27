from src.core.core_logger import core_logger

import pandas as pd

def filter_by_any_multidatas(multidatas: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Filters interactions if any interactions multidatas are in multidatas list
    """
    interactions_filtered = pd.merge(multidatas, interactions, left_on='id_multidata', right_on='multidata_1_id')
    interactions_filtered = interactions_filtered.append(
        pd.merge(multidatas, interactions, left_on='id_multidata', right_on='multidata_2_id'))

    interactions_filtered.drop_duplicates('id_interaction', inplace=True)
    interactions_filtered.reset_index(drop=True, inplace=True)
    return interactions_filtered[interactions.columns.values]


def filter_by_multidatas(multidatas: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Filters interactions if both interactions multidatas are in multidatas list
    """
    interactions_filtered = pd.merge(multidatas, interactions, left_on='id_multidata', right_on='multidata_1_id')
    interactions_filtered = pd.merge(multidatas, interactions_filtered, left_on='id_multidata',
                                     right_on='multidata_2_id')

    interactions_filtered.drop_duplicates('id_interaction', inplace=True)
    interactions_filtered.reset_index(drop=True, inplace=True)

    return interactions_filtered[interactions.columns.values]


# TODO: add test
def filter_by(parameter: str, multidatas: pd.DataFrame, interactions: pd.DataFrame, suffix: ()) -> pd.DataFrame:
    """
    Filters interactions if both interactions multidatas are in multidatas list
    """
    interactions_filtered = pd.merge(multidatas, interactions, left_on=parameter, right_on='{}_{}')
    interactions_filtered = pd.merge(multidatas, interactions_filtered, left_on=parameter,
                                     right_on='multidata_2_id')

    interactions_filtered.drop_duplicates('id_interaction', inplace=True)
    interactions_filtered.reset_index(drop=True, inplace=True)

    return interactions_filtered[interactions.columns.values]


def filter_by_min_score2(interactions: pd.DataFrame, min_score2: float):
    filtered_interactions = interactions[interactions['score_2'] > min_score2]

    return filtered_interactions


def filter_by_receptor_ligand_integrin(proteins: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame of enabled integrin interactions
    """
    core_logger.debug('Filtering by integrin')
    multidata_receptors = proteins[proteins['integrin_interaction']]

    receptor_interactions = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                     right_on='multidata_1_id')
    enabled_interactions = pd.merge(proteins, receptor_interactions, left_on='id_multidata',
                                    right_on='multidata_2_id', suffixes=['_ligands', '_receptors'])

    receptor_interactions_inverted = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                              right_on='multidata_2_id')

    enabled_interactions_inverted = pd.merge(proteins, receptor_interactions_inverted, left_on='id_multidata',
                                             right_on='multidata_1_id', suffixes=['_ligands', '_receptors'])

    enabled_interactions = enabled_interactions.append(enabled_interactions_inverted).reset_index(drop=True)

    enabled_interactions.drop_duplicates(inplace=True)

    return enabled_interactions


def filter_by_is_interactor(interactions: pd.DataFrame) -> pd.DataFrame:
    interactions_filtered = interactions[interactions['is_cellphonedb_interactor']]

    return interactions_filtered
