from cellphonedb.models.interaction.properties_interaction import is_receptor_ligand_by_receptor

import pandas as pd


def filter_by_min_score2(interactions, min_score2):
    filtered_interactions = interactions[interactions['score_2'] > min_score2]

    return filtered_interactions


def filter_receptor_ligand_interactions_by_receptor(interactions, receptor):
    """

    :type interactions: pd.DataFrame
    :type receptor: pd.Series
    :type ligand: pd.Series
    :rtype:
    """

    result = interactions[
        interactions.apply(lambda interaction: is_receptor_ligand_by_receptor(interaction, receptor), axis=1)]
    return result
