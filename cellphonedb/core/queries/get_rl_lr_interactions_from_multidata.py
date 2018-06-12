import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.models.interaction import filter_interaction, functions_interaction
from cellphonedb.core.models.multidata import format_multidata, helper_multidata


def call(protein: pd.DataFrame, enable_integrin: bool,
         min_score2: float, complex_by_multidata, interactions, multidatas_expanded) -> pd.DataFrame:
    multidatas = protein.append(
        complex_by_multidata, ignore_index=True)

    core_logger.debug('Finding Enabled Interactions')
    enabled_interactions = _get_rl_lr_interactions(multidatas, min_score2, enable_integrin, interactions,
                                                   multidatas_expanded)

    result_interactions = _result_interactions_table(enabled_interactions)

    return result_interactions


def _get_rl_lr_interactions(multidatas: pd.DataFrame, min_score_2: float, enable_integrin: bool, interactions,
                            multidatas_expanded) -> pd.DataFrame:
    filtered_interactions = interactions[interactions['score_2'] > min_score_2]

    filtered_interactions = filter_interaction.filter_by_any_multidatas(multidatas, filtered_interactions)

    multidata_interactions = functions_interaction.expand_interactions_multidatas(filtered_interactions,
                                                                                  multidatas_expanded)
    enabled_interactions = filter_interaction.filter_by_receptor_ligand_ligand_receptor(multidata_interactions,
                                                                                        enable_integrin)

    return enabled_interactions


def _result_interactions_table(enabled_interactions: pd.DataFrame) -> pd.DataFrame:
    output_colums = ['id_interaction', 'receptor', 'secreted_ligand', 'source']
    if enabled_interactions.empty:
        return pd.DataFrame(
            columns=output_colums)
    result = pd.DataFrame()
    result['id_interaction'] = enabled_interactions['id_interaction']
    result['receptor'] = enabled_interactions.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_receptor'), axis=1)

    def set_uniprot_value(interaction, suffix):
        if interaction['is_complex{}'.format(suffix)]:
            return ''

        return interaction['name{}'.format(suffix)]

    def set_ensembl_value(interaction, suffix):
        if interaction['is_complex{}'.format(suffix)]:
            return ''

        return interaction['ensembl{}'.format(suffix)]

    result['receptor_uniprot'] = enabled_interactions.apply(
        lambda interaction: set_uniprot_value(interaction, '_receptor'), axis=1)

    result['receptor_ensembl'] = enabled_interactions.apply(
        lambda interaction: set_ensembl_value(interaction, '_receptor'), axis=1)

    result['ligand'] = enabled_interactions.apply(
        lambda interaction: format_multidata.get_value_with_prefix(interaction, '_ligand'), axis=1)

    result['ligand_uniprot'] = enabled_interactions.apply(
        lambda interaction: set_uniprot_value(interaction, '_ligand'), axis=1)

    result['ligand_ensembl'] = enabled_interactions.apply(
        lambda interaction: set_ensembl_value(interaction, '_ligand'), axis=1)

    result['secreted_ligand'] = enabled_interactions['secretion_ligand']

    result['source'] = enabled_interactions['source']
    result.drop_duplicates(inplace=True)

    return result[output_colums]
