import typing

import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction
from cellphonedb.core.queries.query_utils import apply_threshold, merge_cellphone_genes, \
    get_complex_involved_in_counts, filter_empty_cluster_counts, get_cluster_combinations
from utilities import dataframe_format


def call(cluster_counts: pd.DataFrame, threshold: float, enable_complex: bool, complex_composition: pd.DataFrame,
         genes_expanded: pd.DataFrame, complex_expanded: pd.DataFrame,
         interactions_expanded: pd.DataFrame) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
    print('Receptor Ligand Integrin Interactions')
    clusters_names = cluster_counts.columns.values
    cluster_counts_cellphone = merge_cellphone_genes(cluster_counts, genes_expanded)

    cluster_counts_filtered = apply_threshold(cluster_counts_cellphone, clusters_names, threshold)

    cluster_counts_filtered = filter_empty_cluster_counts(cluster_counts_filtered, clusters_names)

    if enable_complex:
        cluster_counts_filtered['is_complex'] = False
        complex_counts = get_complex_involved_in_counts(cluster_counts_filtered, clusters_names,
                                                        complex_composition,
                                                        complex_expanded)
        cluster_counts_filtered = cluster_counts_filtered.append(complex_counts)

    print('Cluster Interactions')
    cluster_interactions = get_cluster_combinations(clusters_names)

    print('Finding Enabled Interactions')
    enabled_interactions = _get_enabled_interactions(cluster_counts_filtered, interactions_expanded)

    result_interactions = _result_interactions_table(cluster_interactions, enabled_interactions)
    result_interactions_extended = _result_interactions_extended_table(enabled_interactions, clusters_names,
                                                                       cluster_counts_filtered, complex_composition)

    return result_interactions, result_interactions_extended


def _result_interactions_extended_table(interactions, clusters_names, cluster_counts, complex_composition):
    result_receptor_complex = _get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions,
                                                                '_receptors', complex_composition)

    result_receptor = interactions.loc[interactions['is_complex_receptors'] == False][
        ['id_interaction', 'entry_name_receptors', 'name_receptors', 'gene_name_receptors', 'is_complex_receptors'] + [
            cluster_name + '_receptors' for cluster_name in clusters_names]]

    def remove_suffix(column_name, suffix):
        if column_name.endswith(suffix):
            return column_name[:-len(suffix)]

        return column_name

    result_receptor.rename(columns=lambda column_name: remove_suffix(column_name, '_receptors'), inplace=True)

    result_receptor = result_receptor.append(result_receptor_complex)
    result_receptor = result_receptor.assign(receptor_ligand='receptor')

    result_ligand_complex = _get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions, '_ligands',
                                                              complex_composition)

    result_ligand = interactions.loc[interactions['is_complex_ligands'] == False][
        ['id_interaction', 'entry_name_ligands', 'name_ligands', 'gene_name_ligands', 'is_complex_ligands'] + [
            cluster_name + '_ligands' for cluster_name in clusters_names]]

    result_ligand.rename(columns=lambda column_name: remove_suffix(column_name, '_ligands'), inplace=True)
    result_ligand = result_ligand.append(result_ligand_complex)
    result_ligand = result_ligand.assign(receptor_ligand='ligand')

    result = result_receptor.append(result_ligand)
    result = dataframe_format.bring_columns_to_start(['id_interaction'], result)
    result.drop_duplicates(inplace=True)

    return result


def _get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions, suffix, complex_composition):
    receptor_complex_interactions = interactions.loc[interactions['is_complex%s' % suffix] == True]
    receptor_complex_interactions = pd.merge(receptor_complex_interactions, complex_composition,
                                             left_on='id_multidata%s' % suffix, right_on='complex_multidata_id')
    receptor_complex_interactions = pd.merge(receptor_complex_interactions, cluster_counts,
                                             left_on='protein_multidata_id', right_on='id_multidata')
    result_receptor_complex = receptor_complex_interactions[
        ['id_interaction', 'entry_name', 'name', 'gene_name', 'name%s' % suffix] + list(clusters_names)]
    result_receptor_complex = result_receptor_complex.rename(columns={'name%s' % suffix: 'complex_name'}, index=str)
    result_receptor_complex = result_receptor_complex.assign(is_complex=True)
    return result_receptor_complex


def _result_interactions_table(cluster_interactions, enabled_interactions):
    """

    :type cluster_interactions: list
    :type enabled_interactions: pd.DataFrame
    :rtype: pd.DataFrame
    """

    result = enabled_interactions['id_interaction']
    cluster_interactions_columns_names = []
    for cluster_interaction in cluster_interactions:
        print(cluster_interaction)
        cluster_interaction_column_name = '%s - %s' % (cluster_interaction[0], cluster_interaction[1])
        cluster_interactions_columns_names.append(cluster_interaction_column_name)
        cluster_interaction_result = _check_receptor_ligand_interactions(cluster_interaction, enabled_interactions,
                                                                         cluster_interaction_column_name)

        result = pd.concat([result, cluster_interaction_result], axis=1)

    result['receptor'] = enabled_interactions['entry_name_receptors'].apply(
        lambda value: 'single:%s' % value)
    result.loc[enabled_interactions['is_complex_receptors'], ['receptor']] = \
        enabled_interactions['name_receptors'].apply(lambda value: 'complex:%s' % value)

    result['ligand'] = enabled_interactions['entry_name_ligands'].apply(lambda value: 'single:%s' % value)
    result.loc[enabled_interactions['is_complex_ligands'], ['ligand']] = enabled_interactions['name_ligands'].apply(
        lambda value: 'complex:%s' % value)

    result['iuphar_ligand'] = enabled_interactions['iuhpar_ligand_ligands']
    result['secreted_ligand'] = enabled_interactions['secretion_ligands']

    result['source'] = enabled_interactions['source']
    result['interaction_ratio'] = result[cluster_interactions_columns_names].apply(
        lambda row: sum(row.astype('bool')) / len(cluster_interactions_columns_names), axis=1)

    if 'is_integrin' in enabled_interactions:
        result['is_integrin'] = enabled_interactions['is_integrin']

    result.drop_duplicates(inplace=True)
    result.sort_values('interaction_ratio', inplace=True)

    result = dataframe_format.bring_columns_to_start(['id_interaction', 'receptor', 'ligand'], result)

    return result


def _check_receptor_ligand_interactions(cluster_interaction, enabled_interactions, clusters_interaction_name):
    receptor_cluster_name = cluster_interaction[0]
    ligand_cluster_name = cluster_interaction[1]

    def get_relation_score(row):
        count_receptor = row['%s_receptors' % receptor_cluster_name]
        count_ligand = row['%s_ligands' % ligand_cluster_name]

        row[clusters_interaction_name] = min(count_receptor, count_ligand)
        return row

    result = enabled_interactions.apply(get_relation_score, axis=1)

    return result[[clusters_interaction_name]]


def _get_enabled_interactions(cluster_counts: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    enabled_interactions = filter_interaction.filter_by_integrin(cluster_counts, interactions)

    return enabled_interactions
