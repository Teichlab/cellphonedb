from cellphonedb.models.interaction import functions_interaction, filter_interaction
from cellphonedb.models.multidata import format_multidata


def call(interactions_expanded):
    interactions_filtered = filter_interaction.filter_receptor_ligand_ligand_receptor(interactions_expanded)

    if interactions_filtered.empty:
        return interactions_filtered

    result = interactions_filtered.loc[:,
             [
                 'name_1', 'entry_name_1', 'secretion_1', 'transmembrane_1', 'iuhpar_ligand_1',
                 'name_2', 'entry_name_2', 'secretion_2', 'transmembrane_2', 'iuhpar_ligand_2',
                 'score_1', 'score_2', 'source', 'comments_interaction'
             ]]

    result['name_1'] = interactions_filtered.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_1'), axis=1)
    result['name_2'] = interactions_filtered.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_2'), axis=1)

    return result
