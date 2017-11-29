import pandas as pd


def merge_interactions(interactions_1, interactions_2, interaction_1_key='protein_2', interaction_2_key='protein_2'):
    '''
    Merges two interactions dataframens prioritizing keeping first on duplicates
    :type interactions_1: pd.DataFrame
    :type interactions_2: pd.DataFrame
    :rtype: pd.DataFrame
    '''

    def interaction_exist(interaction):
        '''
        Checks if interaction already exists in first dataframe.
        :type interaction: pd.Series
        :rtype: pd.Series
        '''
        if len(interactions_1[(interactions_1[interaction_1_key] == interaction[interaction_1_key]) & (
                    interactions_1[interaction_2_key] == interaction[interaction_2_key])]):
            return True

        if len(interactions_1[(interactions_1[interaction_2_key] == interaction[interaction_1_key]) & (
                    interactions_1[interaction_1_key] == interaction[interaction_2_key])]):
            return True

        return False

    interactions_2_not_in_1 = interactions_2[interactions_2.apply(interaction_exist, axis=1) == False]

    interactions = interactions_1.append(interactions_2_not_in_1)

    return interactions
