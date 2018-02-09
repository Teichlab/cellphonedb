from cellphonedb.models.interaction import properties_interaction

import pandas as pd


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


def _filter_by_integrin(proteins, interactions):
    """

    :type proteins: pd.DataFrame
    :type interactions: pd.DataFrame
    :rtype: pd.DataFrame
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
