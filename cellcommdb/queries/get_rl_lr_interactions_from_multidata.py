import pandas as pd

from cellcommdb.models.multidata import format_multidata
from cellcommdb.repository import interaction_repository, complex_repository, multidata_repository

from utilities import dataframe_format


def call(protein: pd.Series, min_score2: float) -> pd.DataFrame:
    print('Get receptor')

    protein = protein.to_frame().transpose()
    print('Finding Complexes')
    multidatas = protein.append(
        complex_repository.get_complex_by_multidatas(protein, False), ignore_index=True)

    print('Finding Enabled Interactions')
    enabled_interactions = _get_rl_lr_interactions(multidatas, min_score2)

    result_interactions = _result_interactions_table(enabled_interactions)

    return result_interactions


def _result_interactions_table(enabled_interactions: pd.DataFrame) -> pd.DataFrame:
    if enabled_interactions.empty:
        return pd.DataFrame(
            columns=['id_interaction', 'receptor', 'iuhpar_ligand', 'iuphar_ligand', 'secreted_ligand', 'source'])
    result = pd.DataFrame()
    result['id_interaction'] = enabled_interactions['id_interaction']
    result['receptor'] = enabled_interactions.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_receptors'), axis=1)

    def set_uniprot_value(interaction, suffix):
        if interaction['is_complex{}'.format(suffix)]:
            return ''

        return interaction['name{}'.format(suffix)]

    def set_ensembl_value(interaction, suffix):
        if interaction['is_complex{}'.format(suffix)]:
            return ''

        return interaction['ensembl{}'.format(suffix)]

    result['receptor_uniprot'] = enabled_interactions.apply(
        lambda interaction: set_uniprot_value(interaction, '_receptors'), axis=1)

    result['receptor_ensembl'] = enabled_interactions.apply(
        lambda interaction: set_ensembl_value(interaction, '_receptors'), axis=1)

    result['ligand'] = enabled_interactions.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_ligands'), axis=1)

    result['ligand_uniprot'] = enabled_interactions.apply(
        lambda interaction: set_uniprot_value(interaction, '_ligands'), axis=1)

    result['ligand_ensembl'] = enabled_interactions.apply(
        lambda interaction: set_ensembl_value(interaction, '_ligands'), axis=1)

    result['iuphar_ligand'] = enabled_interactions['iuhpar_ligand_ligands']
    result['secreted_ligand'] = enabled_interactions['secretion_ligands']

    result['source'] = enabled_interactions['source']
    result.drop_duplicates(inplace=True)
    result = dataframe_format.bring_columns_to_start(['id_interaction', 'receptor', 'ligand'], result)

    return result


def _get_rl_lr_interactions(multidatas: pd.DataFrame, min_score_2: float) -> pd.DataFrame:
    interactions = interaction_repository.get_all()
    interactions = interactions[interactions['score_2'] > min_score_2]
    all_multidatas = multidata_repository.get_all_expanded()
    enabled_interactions = _get_receptor_ligand_interactions(multidatas, interactions, all_multidatas)
    enabled_interactions = enabled_interactions.append(
        _get_ligand_receptor_interactions(multidatas, interactions, all_multidatas), ignore_index=True)

    return enabled_interactions


def _get_ligand_receptor_interactions(multidatas: pd.DataFrame, interactions: pd.DataFrame,
                                      all_multidatas: pd.DataFrame) -> pd.DataFrame:
    multidata_ligands = multidatas[multidatas['is_cellphone_ligand']]
    all_multidata_receptors = all_multidatas[all_multidatas['is_cellphone_receptor']]

    ligand_interactions = pd.merge(multidata_ligands, interactions, left_on='id_multidata', right_on='multidata_1_id')
    enabled_interactions = pd.merge(all_multidata_receptors, ligand_interactions, left_on='id_multidata',
                                    right_on='multidata_2_id', suffixes=['_receptors', '_ligands'])

    ligands_interactions_inverted = pd.merge(multidata_ligands, interactions, left_on='id_multidata',
                                             right_on='multidata_2_id')
    enabled_interactions_inverted = pd.merge(all_multidata_receptors, ligands_interactions_inverted,
                                             left_on='id_multidata', right_on='multidata_1_id',
                                             suffixes=['_receptors', '_ligands'])

    enabled_interactions = enabled_interactions.append(enabled_interactions_inverted).reset_index(drop=True)

    return enabled_interactions


def _get_receptor_ligand_interactions(multidatas: pd.DataFrame, interactions: pd.DataFrame,
                                      all_multidatas: pd.DataFrame) -> pd.DataFrame:
    multidata_receptors = multidatas[multidatas['is_cellphone_receptor']]
    all_multidata_ligands = all_multidatas[all_multidatas['is_cellphone_ligand']]

    receptor_interactions = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                     right_on='multidata_1_id')
    enabled_interactions = pd.merge(all_multidata_ligands, receptor_interactions, left_on='id_multidata',
                                    right_on='multidata_2_id', suffixes=['_ligands', '_receptors'])

    receptor_interactions_inverted = pd.merge(multidata_receptors, interactions, left_on='id_multidata',
                                              right_on='multidata_2_id')
    enabled_interactions_inverted = pd.merge(all_multidata_ligands, receptor_interactions_inverted,
                                             left_on='id_multidata', right_on='multidata_1_id',
                                             suffixes=['_ligands', '_receptors'])

    enabled_interactions = enabled_interactions.append(enabled_interactions_inverted).reset_index(drop=True)

    return enabled_interactions
