from cellphonedb.core.models.interaction import properties_interaction

import pandas as pd

from cellphonedb.core.models.interaction.properties_interaction import is_receptor_ligand
from utils import dataframe_format


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


def filter_by_min_score2(interactions, min_score2):
    filtered_interactions = interactions[interactions['score_2'] > min_score2]

    return filtered_interactions


def filter_receptor_ligand_interactions_by_receptor(interactions: pd.DataFrame, receptor: pd.Series) -> pd.DataFrame:
    result = interactions[
        interactions.apply(
            lambda interaction: properties_interaction.is_receptor_ligand_by_receptor(interaction, receptor), axis=1)]
    return result


def filter_receptor_ligand_ligand_receptor(interactions_expanded: pd.DataFrame, suffix=['_1', '_2']) -> pd.DataFrame:
    result = interactions_expanded[interactions_expanded.apply(
        lambda interaction: properties_interaction.is_receptor_ligand_or_ligand_receptor(interaction, suffix), axis=1)]

    return result


def filter_by_receptor_ligand_integrin(proteins: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame of enabled integrin interactions
    """
    print('Filtering by integrin')
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


def filter_by_receptor_ligand_ligand_receptor(interactions: pd.DataFrame, enable_integrin: bool,
                                              avoid_duplited: bool = True) -> pd.DataFrame:
    """
    return a table of receptor ligand interactons
    """
    interactions = interactions.rename(index=str, columns={'score_1': 'score_one', 'score_2': 'score_two'})

    interactions_enabled_rl = interactions[
        interactions.apply(
            lambda interaction: is_receptor_ligand(interaction, enable_integrin=enable_integrin, receptor_suffix='_1',
                                                   ligand_suffix='_2', score_two_suffix='_two'), axis=1)]
    interactions_enabled_rl = dataframe_format.change_column_suffix(interactions_enabled_rl, '_1', '_receptor')
    interactions_enabled_rl = dataframe_format.change_column_suffix(interactions_enabled_rl, '_2', '_ligand')

    interactions_enabled_lr = interactions[
        interactions.apply(
            lambda interaction: is_receptor_ligand(interaction, enable_integrin=enable_integrin, receptor_suffix='_2',
                                                   ligand_suffix='_1', score_two_suffix='_two'), axis=1)].copy()
    interactions_enabled_lr = dataframe_format.change_column_suffix(interactions_enabled_lr, '_2', '_receptor')
    interactions_enabled_lr = dataframe_format.change_column_suffix(interactions_enabled_lr, '_1', '_ligand')

    interactions_enabled = interactions_enabled_rl.append(interactions_enabled_lr)

    interactions_enabled = interactions_enabled.rename(index=str,
                                                       columns={'score_one': 'score_1', 'score_two': 'score_2'})
    interactions_enabled.drop_duplicates(['id_multidata_receptor', 'id_multidata_ligand'], inplace=True)
    if avoid_duplited:
        interactions_enabled.drop_duplicates(['id_interaction'], inplace=True)
    interactions_enabled.reset_index(drop=True, inplace=True)

    return interactions_enabled
