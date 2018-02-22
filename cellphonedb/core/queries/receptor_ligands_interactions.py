import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction
from cellphonedb.core.queries import query_utils
from cellphonedb.core.queries.query_utils import get_counts_proteins_of_complexes
from utilities import dataframe_format


def call(cluster_counts, threshold, enable_integrin, enable_transmembrane, enable_secreted, enable_complex,
         complex_composition, genes_expanded, complex_expanded, interactions_expanded, clusters_names=None):
    print('Receptor Ligands Interactions Initializated')
    if not clusters_names:
        clusters_names = cluster_counts.columns.values
    cluster_counts_cellphone = query_utils.merge_cellphone_genes(cluster_counts, genes_expanded)

    cluster_counts_filtered = query_utils.apply_threshold(cluster_counts_cellphone, clusters_names, threshold)

    cluster_counts_filtered = query_utils.filter_empty_cluster_counts(cluster_counts_filtered, clusters_names)

    if enable_complex:
        print('Finding Complexes')
        cluster_counts_filtered['is_complex'] = False
        complex_counts = query_utils.get_complex_involved_in_counts(cluster_counts_filtered, clusters_names,
                                                                    complex_composition, complex_expanded)
        cluster_counts_filtered = cluster_counts_filtered.append(
            complex_counts)

    print('Cluster Interactions')
    cluster_interactions = query_utils.get_cluster_combinations(clusters_names)

    print('Finding Enabled Interactions')
    enabled_interactions = _get_enabled_interactions(cluster_counts_filtered, interactions_expanded, 0.3,
                                                     enable_integrin, enable_transmembrane, enable_secreted)

    result_interactions = _result_interactions_table(cluster_interactions, enabled_interactions)
    result_interactions_extended = _result_interactions_extended_table(enabled_interactions, clusters_names,
                                                                       cluster_counts_filtered, complex_composition)

    return result_interactions, result_interactions_extended


def _result_interactions_extended_table(interactions, clusters_names, cluster_counts, complex_composition):
    if interactions.empty:
        return pd.DataFrame(columns=['id_interaction', 'complex_name', 'entry_name', 'gene_name', 'is_complex', 'name',
                                     'receptor_ligand'] + list(clusters_names))
    result_receptor_complex = get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions,
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

    result_ligand_complex = get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions, '_ligands',
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

    if result.empty:
        return pd.DataFrame(
            columns=list(result.columns.values) + ['receptor', 'ligand', 'iuphar_ligand', 'secreted_ligand', 'source',
                                                   'interaction_ratio', 'enabled_by_integrin',
                                                   'enabled_by_transmembrane', 'enabled_by_secreted'])

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

    result['enabled_by_integrin'] = enabled_interactions['enabled_by_integrin']
    result['enabled_by_transmembrane'] = enabled_interactions['enabled_by_transmembrane']
    result['enabled_by_secreted'] = enabled_interactions['enabled_by_secreted']

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
    if result.empty:
        result = pd.DataFrame(columns=[clusters_interaction_name])

    return result[[clusters_interaction_name]]


def _get_enabled_interactions(cluster_counts, interactions, min_score_2, enable_integrin, enable_transmembrane,
                              enable_secreted):
    result_columns = list(interactions.columns.values) + [
        'id_multidata_ligands', 'id_multidata_receptors', 'enabled_by_integrin', 'enabled_by_transmembrane',
        'enabled_by_secreted']

    enabled_columns = []

    interactions = interactions[interactions['score_2'] > min_score_2]
    enabled_interactions = pd.DataFrame(columns=result_columns)

    if enable_integrin:
        integrin_interactions = filter_interaction.filter_by_receptor_ligand_integrin(cluster_counts, interactions)
        integrin_interactions['enabled_by_integrin'] = True
        enabled_columns.append('enabled_by_integrin')
        enabled_interactions = integrin_interactions.append(enabled_interactions)

    if enable_transmembrane:
        transmembrane_interactions = filter_interaction.filter_by_receptor_ligand_transmembrane(cluster_counts,
                                                                                                interactions)
        transmembrane_interactions['enabled_by_transmembrane'] = True
        enabled_columns.append('enabled_by_transmembrane')
        enabled_interactions = transmembrane_interactions.append(enabled_interactions)

    if enable_secreted:
        secreted_interactions = filter_interaction.filter_by_receptor_ligand_secreted(cluster_counts, interactions)
        secreted_interactions['enabled_by_secreted'] = True
        enabled_columns.append('enabled_by_secreted')
        enabled_interactions = secreted_interactions.append(enabled_interactions)

    enabled_interactions[enabled_columns] = \
        enabled_interactions[enabled_columns].fillna(False)

    enabled_interactions.reset_index(drop=True, inplace=True)

    merged_interactions = merge_enabled_interactions(enabled_interactions, enabled_columns)

    return merged_interactions


def merge_enabled_interactions(enabled_interactions: pd.DataFrame, boolean_columns: list) -> pd.DataFrame:
    non_duplicated_interactions = enabled_interactions.drop_duplicates(
        ['id_multidata_ligands', 'id_multidata_receptors'], keep=False)

    duplicated_interactions = enabled_interactions[
        enabled_interactions.duplicated(['id_multidata_ligands', 'id_multidata_receptors'], keep=False)]

    def merge_enabled_values(row):
        values = \
            duplicated_interactions[(duplicated_interactions['id_multidata_ligands'] == row['id_multidata_ligands']) &
                                    (duplicated_interactions['id_multidata_receptors'] == row[
                                        'id_multidata_receptors'])][boolean_columns]

        row[boolean_columns] = values.any(axis=0, skipna=True)

        return row

    unique_interactions = duplicated_interactions.drop_duplicates(['id_multidata_ligands', 'id_multidata_receptors'])
    unique_interactions = unique_interactions.apply(merge_enabled_values, axis=1)

    return non_duplicated_interactions.append(unique_interactions)
