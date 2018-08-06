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
    interactions_normalized = interactions.apply(
        lambda interaction: normalize_interaction(interactions, interaction, interaction_1_key, interaction_2_key),
        axis=1)

    return interactions_normalized


def normalize_interaction(custom_interactions, interaction, interaction_1_key='uniprot_1',
                          interaction_2_key='uniprot_2'):
    """
    Permute interaction if is it necessary.
    """
    if interaction[interaction_2_key] != interaction[interaction_1_key]:
        duplicated_inversed = custom_interactions[
            (custom_interactions[interaction_2_key] == interaction[interaction_1_key]) & (
                    custom_interactions[interaction_1_key] == interaction[interaction_2_key])]

        if len(duplicated_inversed):
            first_interaction_duplicate = duplicated_inversed.iloc[0]

            if first_interaction_duplicate.name < interaction.name:
                interaction[interaction_1_key] = first_interaction_duplicate[interaction_1_key]
                interaction[interaction_2_key] = first_interaction_duplicate[interaction_2_key]

            return interaction

    return interaction
