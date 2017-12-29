from cellphonedb.models.interaction import functions_interaction, filter_interaction
from cellphonedb.repository import interaction_repository


def call():
    interactions = interaction_repository.get_all()
    interactions = functions_interaction.expand_interactions_multidatas(interactions)
    result = filter_interaction.filter_receptor_ligand_ligand_receptor(interactions)

    result = result.loc[:,
             ['score_1', 'score_2', 'source', 'comments_x', 'name_1', 'entry_name_1', 'name_2', 'entry_name_2']]

    result.rename(columns={'comments_x': 'comments'}, inplace=True)
    return result
