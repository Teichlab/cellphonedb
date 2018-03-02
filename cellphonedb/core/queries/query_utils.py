import itertools

import pandas as pd


def apply_threshold(cluster_counts: pd.DataFrame, cluster_names: list, threshold: float) -> pd.DataFrame:
    """
    Sets to 0 minor value colunts than threshold
    """

    print('Aplicating Threshold {}'.format(threshold))
    cluster_counts_filtered = cluster_counts.copy()
    for cluster_name in cluster_names:
        cluster_counts_filtered.loc[
            cluster_counts_filtered[cluster_name] < float(threshold), [cluster_name]] = 0.0

    return cluster_counts_filtered


def merge_cellphone_genes(cluster_counts: pd.DataFrame, genes_expanded: pd.DataFrame) -> pd.DataFrame:
    """
    Merges cluster genes with CellPhoneDB values
    """

    multidata_counts = pd.merge(cluster_counts, genes_expanded, left_index=True, right_on='ensembl')

    return multidata_counts


# TODO: Add a test
def get_complex_involved_in_counts(multidatas_counts: pd.DataFrame, clusters_names: list,
                                   complex_composition: pd.DataFrame,
                                   complex_expanded: pd.DataFrame) -> pd.DataFrame:
    """
    Gets complexes involved in counts
    """
    print('Finding Complexes')
    complex_counts_composition = pd.merge(complex_composition, multidatas_counts, left_on='protein_multidata_id',
                                          right_on='id_multidata')

    # TODO: check if custer counts empty
    def all_protein_involved(complex):
        number_proteins_in_counts = len(
            complex_counts_composition[
                complex_counts_composition['complex_multidata_id'] == complex['complex_multidata_id']])

        if number_proteins_in_counts < complex['total_protein']:
            return False

        return True

    complex_counts_composition = complex_counts_composition[
        complex_counts_composition.apply(all_protein_involved, axis=1)]

    complex_counts_composition = pd.merge(complex_counts_composition, complex_expanded,
                                          left_on='complex_multidata_id',
                                          right_on='id_multidata',
                                          suffixes=['_protein', ''])

    def set_complex_cluster_counts(row):
        scores_complex = complex_counts_composition[
            row['complex_multidata_id'] == complex_counts_composition['complex_multidata_id']]

        for cluster_name in clusters_names:
            row[cluster_name] = scores_complex[cluster_name].min()
        return row

    complex_counts = complex_counts_composition.drop_duplicates(['complex_multidata_id'])

    complex_counts = complex_counts.apply(set_complex_cluster_counts, axis=1)

    complex_counts = complex_counts[list(clusters_names) + list(complex_expanded.columns.values)]

    complex_counts['is_complex'] = True

    complex_counts = filter_empty_cluster_counts(complex_counts, clusters_names)

    return complex_counts


def filter_empty_cluster_counts(cluster_counts: pd.DataFrame, clusters_names: list) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    filetered_cluster_counts = cluster_counts[cluster_counts[clusters_names].apply(lambda row: row.sum() > 0, axis=1)]
    return filetered_cluster_counts


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


def get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions, suffix, complex_composition):
    receptor_complex_interactions = interactions.loc[interactions['is_complex%s' % suffix] == True]
    receptor_complex_interactions = pd.merge(receptor_complex_interactions, complex_composition,
                                             left_on='id_multidata%s' % suffix, right_on='complex_multidata_id')
    receptor_complex_interactions = pd.merge(receptor_complex_interactions, cluster_counts,
                                             left_on='protein_multidata_id', right_on='id_multidata')

    if receptor_complex_interactions.empty:
        return pd.DataFrame()
    result_receptor_complex = receptor_complex_interactions[
        ['id_interaction', 'entry_name', 'name', 'gene_name', 'name%s' % suffix] + list(clusters_names)]
    result_receptor_complex = result_receptor_complex.rename(columns={'name%s' % suffix: 'complex_name'}, index=str)
    result_receptor_complex = result_receptor_complex.assign(is_complex=True)
    return result_receptor_complex
