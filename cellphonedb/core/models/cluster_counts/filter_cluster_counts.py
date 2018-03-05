import pandas as pd


def filter_empty_cluster_counts(cluster_counts: pd.DataFrame, clusters_names: list) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    filetered_cluster_counts = cluster_counts[cluster_counts[clusters_names].apply(lambda row: row.sum() > 0, axis=1)]
    return filetered_cluster_counts
