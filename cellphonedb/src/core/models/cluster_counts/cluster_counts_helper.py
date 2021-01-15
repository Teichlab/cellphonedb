import itertools

import pandas as pd

from cellphonedb.src.core.core_logger import core_logger


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


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
