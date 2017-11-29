import pandas as pd


def interaction_exist(interaction, interactions, interaction_1_key='protein_1', interaction_2_key='protein_2'):
    '''
    Checks if interaction already exists in first dataframe.
    :type interaction: pd.Series
    :type interaction: pd.DataFrame
    :rtype: bool
    '''

    if len(interactions[(interactions[interaction_1_key] == interaction[interaction_1_key]) & (
                interactions[interaction_2_key] == interaction[interaction_2_key])]):
        return True

    if len(interactions[(interactions[interaction_2_key] == interaction[interaction_1_key]) & (
                interactions[interaction_1_key] == interaction[interaction_2_key])]):
        return True

    return False
