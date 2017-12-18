import pandas as pd

from cellcommdb.common.generic_exception import GenericException
from cellcommdb.models.interaction.filter_interaction import filter_by_min_score2, \
    filter_receptor_ligand_interactions_by_receptor
from cellcommdb.models.multidata import format_multidata
from cellcommdb.models.multidata.properties_multidata import is_receptor
from cellcommdb.repository import interaction_repository
from cellcommdb.repository.protein import get_protein_multidata_by_uniprot

# TODO: Extract methods
from utilities import dataframe_format


def call(receptor: str, min_score2: float) -> pd.DataFrame:
    print('Get Ligands From Receptor')

    protein_receptor = get_protein_multidata_by_uniprot(receptor)

    if protein_receptor is None:
        raise GenericException(
            {'code': 'protein_not_found', 'title': 'Protein not found',
             'detail': 'Protein %s doesn\'t exist in Cellphone Database' % receptor})

    if not is_receptor(protein_receptor):
        raise GenericException({'code': 'not_receptor', 'title': 'Protein not receptor',
                                'detail': 'Protein %s is not receptor' % receptor})

    interactions = interaction_repository.get_interactions_multidata_by_multidata_id(protein_receptor['id_protein'])
    interactions = filter_by_min_score2(interactions, min_score2)

    if interactions.empty:
        return interactions
    interactions_receptor_ligand = filter_receptor_ligand_interactions_by_receptor(interactions, protein_receptor)
    return _result_query_interactions(interactions_receptor_ligand, protein_receptor)


def _result_query_interactions(interactions: pd.DataFrame, receptor: pd.Series):
    result_ligand_1 = pd.DataFrame()

    ligand_1 = interactions[interactions['multidata_1_id'] == receptor.id_multidata]

    result_ligand_1['id_interaction'] = ligand_1['id_interaction']
    if not ligand_1.empty:
        result_ligand_1['ligand'] = ligand_1.apply(
            lambda interaction: format_multidata.get_value_with_prefix(interaction, '_1'), axis=1)
        result_ligand_1['receptor'] = ligand_1.apply(
            lambda interaction: format_multidata.get_value_with_prefix(interaction, '_2'), axis=1)
        result_ligand_1['source'] = ligand_1['source']
        result_ligand_1['secreted_ligand'] = ligand_1['secretion_1']
        result_ligand_1['iuphar_ligand'] = ligand_1['ligand_1']

    ligand_2 = interactions[interactions['multidata_2_id'] == receptor.id_multidata]
    result_ligand_2 = pd.DataFrame()
    result_ligand_2['id_interaction'] = ligand_2['id_interaction']
    if not ligand_2.empty:
        result_ligand_2['ligand'] = ligand_2.apply(
            lambda interaction: format_multidata.get_value_with_prefix(interaction, '_2'), axis=1)
        result_ligand_2['receptor'] = ligand_2.apply(
            lambda interaction: format_multidata.get_value_with_prefix(interaction, '_1'), axis=1)
        result_ligand_2['source'] = ligand_2['source']
        result_ligand_2['secreted_ligand'] = ligand_2['secretion_2']
        result_ligand_2['iuphar_ligand'] = ligand_2['ligand_2']

    result = result_ligand_1.append(result_ligand_2, ignore_index=True)
    result = dataframe_format.bring_columns_to_end(['iuphar_ligand', 'source'], result)
    return result
