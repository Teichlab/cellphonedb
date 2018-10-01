import itertools

import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.models.cluster_counts.cluster_counts_filter import filter_empty_cluster_counts
from cellphonedb.src.core.models.complex import complex_helper


def merge_complex_counts(clusters_names: list, complex_counts_composition: pd.DataFrame,
                         complex_columns_names: list) -> pd.DataFrame:
    """
    Merges the counts values of multiple components of complex.
    Sets the minimum cluster value for the components of a complex.
    ie:

    input matrix:
                        cell1   cell2   cell3   cell4
    count1  complex_1   0.1     0.2     0.2     0.1
    count2  complex_2   0.2     0.1     0.5     0.0

    output matrix:
                        cell1   cell2   cell3   cell4
    count1  complex_1   0.1     0.1     0.2     0.0
    count2  complex_2   0.1     0.1     0.2     0.0

    """

    if complex_counts_composition.empty:
        return pd.DataFrame()

    def set_complex_cluster_counts(row):
        scores_complex = complex_counts_composition[
            row['complex_multidata_id'] == complex_counts_composition['complex_multidata_id']]

        for cluster_name in clusters_names:
            row[cluster_name] = scores_complex[cluster_name].min()
        return row

    complex_counts = complex_counts_composition.drop_duplicates(['complex_multidata_id'])
    complex_counts = complex_counts.apply(set_complex_cluster_counts, axis=1)
    complex_counts = complex_counts[clusters_names + complex_columns_names]
    return complex_counts


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


def get_complex_involved_in_counts(multidatas_counts: pd.DataFrame, clusters_names: list,
                                   complex_composition: pd.DataFrame,
                                   complex_expanded: pd.DataFrame) -> pd.DataFrame:
    """
    Gets complexes involved in counts
    """
    core_logger.debug('Finding Complexes')
    complex_counts_composition = complex_helper.get_involved_complex_from_protein(multidatas_counts, complex_expanded,
                                                                                  complex_composition,
                                                                                  drop_duplicates=False)

    complex_counts = merge_complex_counts(clusters_names, complex_counts_composition,
                                          list(complex_expanded.columns.values))
    complex_counts = filter_empty_cluster_counts(complex_counts, clusters_names)

    complex_counts.reset_index(drop=True, inplace=True)

    return complex_counts


def apply_threshold(cluster_counts: pd.DataFrame, cluster_names: list, threshold: float) -> pd.DataFrame:
    """
    Sets to 0 minor value colunts than threshold
    """

    core_logger.debug('Aplicating Threshold {}'.format(threshold))
    cluster_counts_filtered = cluster_counts.copy()
    for cluster_name in cluster_names:
        cluster_counts_filtered.loc[
            cluster_counts_filtered[cluster_name] < float(threshold), [cluster_name]] = 0.0

    return cluster_counts_filtered


def expand_multidata(cluster_counts: pd.DataFrame, multidatas: pd.DataFrame) -> pd.DataFrame:
    expanded = pd.merge(cluster_counts, multidatas, left_on='id_multidata', right_on='id_multidata')
    expanded = expanded.drop_duplicates().reset_index(drop=True)

    return expanded
