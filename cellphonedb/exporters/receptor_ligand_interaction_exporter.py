from cellphonedb.models.interaction import functions_interaction, filter_interaction
from cellphonedb.models.multidata import format_multidata
from cellphonedb.repository import interaction_repository


def call():
    interactions = interaction_repository.get_all()
    interactions = functions_interaction.expand_interactions_multidatas(interactions)
    interactions_filtered = filter_interaction.filter_receptor_ligand_ligand_receptor(interactions)

    result = interactions_filtered.loc[:,
             [
                 'name_1', 'entry_name_1', 'secretion_1', 'transmembrane_1', 'iuhpar_ligand_1',
                 'name_2', 'entry_name_2', 'secretion_2', 'transmembrane_2', 'iuhpar_ligand_2',
                 'score_1', 'score_2', 'source', 'comments_x'
             ]]

    result['name_1'] = interactions_filtered.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_1'), axis=1)
    result['name_2'] = interactions_filtered.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_2'), axis=1)

    result.rename(columns={'comments_x': 'comments'}, inplace=True)
    return result
