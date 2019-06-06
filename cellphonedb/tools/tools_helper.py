import pandas as pd


def interaction_exist(interaction, interactions, interaction_1_key='uniprot_1', interaction_2_key='uniprot_2'):
    """
    Checks if interaction already exists in first dataframe.
    """

    if len(interactions[(interactions[interaction_1_key] == interaction[interaction_1_key]) & (
            interactions[interaction_2_key] == interaction[interaction_2_key])]):
        return True

    if len(interactions[(interactions[interaction_2_key] == interaction[interaction_1_key]) & (
            interactions[interaction_1_key] == interaction[interaction_2_key])]):
        return True

    return False


def sort_interactions_partners_alphabetically(interactions: pd.DataFrame,
                                              names: tuple = ('partner_1', 'partner_2')) -> pd.DataFrame:
    """
    Sorts interactions partners alphabetically:
    ie:
    A->B        A->B
    B->C        B->C
    D->A   =>   A->D
    B->A        A->B
    E->D        D->E
    """
    interactions = interactions.copy()

    def alphabetic_sort(interaction: pd.Series):
        return pd.Series({
            names[0]: min([interaction[names[0]], interaction[names[1]]]),
            names[1]: max([interaction[names[0]], interaction[names[1]]])
        })

    interactions[[names[0], names[1]]] = interactions.apply(alphabetic_sort, axis=1)

    return interactions


def normalize_interactions(interactions, interaction_1_key='protein_1', interaction_2_key='protein_2'):
    """
    Permutes all inversed interactions:
    ie:
    A->B        A->B
    B->A        A->B
    B->A   =>   A->B
    A->B        A->B
    B->A        A->B

    """
    return sort_interactions_partners_alphabetically(interactions, (interaction_1_key, interaction_2_key))
