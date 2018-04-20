import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.models.cluster_counts import helper_cluster_counts, filter_cluster_counts
from cellphonedb.core.models.interaction import filter_interaction, functions_interaction
from cellphonedb.core.queries.query_utils import get_counts_proteins_of_complexes
from utils import dataframe_format


def call(cluster_counts: pd.DataFrame, threshold: float, enable_integrin: bool, enable_complex: bool,
         complex_composition: pd.DataFrame, genes_expanded: pd.DataFrame, complex_expanded: pd.DataFrame,
         interactions: pd.DataFrame, clusters_names: list = None) -> (pd.DataFrame, pd.DataFrame):
    core_logger.debug('Receptor Ligands Interactions Initializated')
    if not clusters_names:
        clusters_names = list(cluster_counts.columns.values)
        clusters_names.remove('gene')
    cluster_counts_cellphone = filter_cluster_counts.filter_by_gene(cluster_counts, genes_expanded)
    cluster_counts_filtered = helper_cluster_counts.apply_threshold(cluster_counts_cellphone, clusters_names, threshold)
    cluster_counts_filtered = filter_cluster_counts.filter_empty_cluster_counts(cluster_counts_filtered, clusters_names)

    if enable_complex:
        core_logger.debug('Finding Complexes')
        complex_counts = helper_cluster_counts.get_complex_involved_in_counts(cluster_counts_filtered, clusters_names,
                                                                              complex_composition, complex_expanded)
        cluster_counts_filtered = cluster_counts_filtered.append(
            complex_counts)

    core_logger.debug('Cluster Interactions')
    cluster_interactions = helper_cluster_counts.get_cluster_combinations(clusters_names)

    core_logger.debug('Finding Enabled Interactions')
    count_interactions = filter_interaction.filter_by_multidatas(cluster_counts_filtered, interactions)
    count_interactions = functions_interaction.expand_interactions_multidatas(count_interactions,
                                                                              cluster_counts_filtered)
    enabled_interactions = filter_interaction.filter_by_receptor_ligand_ligand_receptor(count_interactions,
                                                                                        enable_integrin)

    result_interactions = _result_interactions_table(cluster_interactions, enabled_interactions)
    result_interactions_extended = _result_interactions_extended_table(enabled_interactions, clusters_names,
                                                                       cluster_counts_filtered, complex_composition)

    return result_interactions, result_interactions_extended


def _result_interactions_extended_table(interactions, clusters_names, cluster_counts, complex_composition):
    output_columns = ['id_interaction', 'complex_name', 'entry_name', 'gene_name', 'is_complex', 'name',
                      'receptor_ligand'] + list(clusters_names)

    if interactions.empty:
        return pd.DataFrame(columns=output_columns)

    receptors = _result_extended_part(cluster_counts, clusters_names, complex_composition, interactions, '_receptor')
    receptors['receptor_ligand'] = 'receptor'
    ligands = _result_extended_part(cluster_counts, clusters_names, complex_composition, interactions, '_ligand')
    ligands['receptor_ligand'] = 'ligand'

    extended_proteins = receptors.append(ligands)

    if not 'complex_name' in extended_proteins:
        extended_proteins['complex_name'] = pd.np.NaN

    return extended_proteins[output_columns]


def _result_extended_part(cluster_counts: pd.DataFrame, clusters_names: list, complex_composition: pd.DataFrame,
                          interactions: pd.DataFrame, suffix: str) -> pd.DataFrame:
    complex_multidatas = pd.DataFrame()
    complex_multidatas[['id_interaction', 'id_multidata', 'name']] = \
        interactions[interactions['is_complex{}'.format(suffix)]][
            ['id_interaction', 'id_multidata{}'.format(suffix), 'name{}'.format(suffix)]]
    complexes = get_counts_proteins_of_complexes(cluster_counts, complex_multidatas, complex_composition)
    multidatas = pd.DataFrame()
    multidatas[['id_interaction', 'id_multidata']] = \
        interactions[interactions['is_complex{}'.format(suffix)] == False][
            ['id_interaction', 'id_multidata{}'.format(suffix)]]
    non_complex = pd.merge(multidatas, cluster_counts, on='id_multidata')
    result = non_complex.append(complexes)

    return result


def _result_interactions_table(cluster_interactions, enabled_interactions):
    """

    :type cluster_interactions: list
    :type enabled_interactions: pd.DataFrame
    :rtype: pd.DataFrame
    """

    result_cluster_interactions_names = [('{} - {}'.format(cluster_interaction[0], cluster_interaction[1])) for
                                         cluster_interaction in cluster_interactions]

    empty_result = pd.DataFrame(
        columns=['id_interaction', 'receptor', 'ligand', 'secreted_ligand', 'source',
                 'interaction_ratio', 'is_integrin'] + result_cluster_interactions_names)

    if enabled_interactions.empty:
        return empty_result

    result = enabled_interactions['id_interaction']
    cluster_interactions_columns_names = []
    for cluster_interaction in cluster_interactions:
        cluster_interaction_column_name = '%s - %s' % (cluster_interaction[0], cluster_interaction[1])
        cluster_interactions_columns_names.append(cluster_interaction_column_name)
        cluster_interaction_result = _check_receptor_ligand_interactions(cluster_interaction, enabled_interactions,
                                                                         cluster_interaction_column_name)

        result = pd.concat([result, cluster_interaction_result], axis=1)

    if result.empty:
        return empty_result

    result = _format_result_interaction(cluster_interactions_columns_names, enabled_interactions, result)

    return result


def _format_result_interaction(cluster_interactions_columns_names, enabled_interactions, result):
    result['receptor'] = enabled_interactions['entry_name_receptor'].apply(
        lambda value: 'single:%s' % value)
    result.loc[enabled_interactions['is_complex_receptor'], ['receptor']] = \
        enabled_interactions['name_receptor'].apply(lambda value: 'complex:%s' % value)
    result['ligand'] = enabled_interactions['entry_name_ligand'].apply(lambda value: 'single:%s' % value)
    result.loc[enabled_interactions['is_complex_ligand'], ['ligand']] = enabled_interactions['name_ligand'].apply(
        lambda value: 'complex:%s' % value)
    result['secreted_ligand'] = enabled_interactions['secretion_ligand']
    result['source'] = enabled_interactions['source']
    result['interaction_ratio'] = result[cluster_interactions_columns_names].apply(
        lambda row: sum(row.astype('bool')) / len(cluster_interactions_columns_names), axis=1)
    result['is_integrin'] = enabled_interactions['integrin_interaction_receptor'] | enabled_interactions[
        'integrin_interaction_ligand']
    result.drop_duplicates(inplace=True)
    result.sort_values('interaction_ratio', inplace=True)
    result = dataframe_format.bring_columns_to_start(['id_interaction', 'receptor', 'ligand'], result)
    return result


# TODO: test individually
def _check_receptor_ligand_interactions(cluster_interaction, enabled_interactions, clusters_interaction_name):
    receptor_cluster_name = cluster_interaction[0]
    ligand_cluster_name = cluster_interaction[1]

    def get_relation_score(row):
        count_receptor = row['%s_receptor' % receptor_cluster_name]
        count_ligand = row['%s_ligand' % ligand_cluster_name]

        row[clusters_interaction_name] = min(count_receptor, count_ligand)
        return row

    result = enabled_interactions.apply(get_relation_score, axis=1)
    if result.empty:
        result = pd.DataFrame(columns=[clusters_interaction_name])

    return result[[clusters_interaction_name]]
