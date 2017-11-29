import pandas as pd

from tools.repository.interaction import interaction_exist


def merge_interactions(interactions_1, interactions_2, interaction_1_key='protein_2', interaction_2_key='protein_2'):
    '''
    Merges two interactions dataframens prioritizing keeping first on duplicates
    :type interactions_1: pd.DataFrame
    :type interactions_2: pd.DataFrame
    :rtype: pd.DataFrame
    '''

    interactions_2_not_in_1 = interactions_2[
        interactions_2.apply(lambda row: interaction_exist(row, interactions_1, interaction_1_key, interaction_2_key),
                             axis=1) == False]

    interactions = interactions_1.append(interactions_2_not_in_1)

    return interactions
