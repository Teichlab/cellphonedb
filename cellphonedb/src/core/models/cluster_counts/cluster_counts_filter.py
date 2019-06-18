import pandas as pd


def filter_by_gene(cluster_counts: pd.DataFrame, genes: pd.DataFrame, counts_data: str = 'ensembl') -> pd.DataFrame:
    """
    Returns only the clusters in genes
    """

    right_column = counts_data

    clusters_filtered = pd.merge(cluster_counts, genes, left_on='gene', right_on=right_column)

    clusters_filtered.drop(right_column, inplace=True, axis=1)

    return clusters_filtered


def filter_empty_cluster_counts(counts: pd.DataFrame, clusters_names: list) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    if counts.empty:
        return counts

    filtered_counts = counts[counts[clusters_names].apply(lambda row: row.sum() > 0, axis=1)]
    return filtered_counts
