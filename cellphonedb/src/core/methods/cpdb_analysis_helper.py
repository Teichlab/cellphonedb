import pandas as pd
import numpy as np

def percent_analysis(clusters: dict,
                     threshold: float,
                     interactions: pd.DataFrame,
                     cluster_interactions: list,
                     base_result: pd.DataFrame,
                     separator: str,
                     ) -> pd.DataFrame:
    GENE_ID1 = 'multidata_1_id'
    GENE_ID2 = 'multidata_2_id'

    cluster1_names = cluster_interactions[:, 0]
    cluster2_names = cluster_interactions[:, 1]
    gene1_ids = interactions[GENE_ID1].values
    gene2_ids = interactions[GENE_ID2].values

    x = clusters['percents'].loc[gene1_ids, cluster1_names].values
    y = clusters['percents'].loc[gene2_ids, cluster2_names].values

    result = pd.DataFrame(
        ((x > threshold) * (y > threshold)).astype(int),
        index=interactions.index,
        columns=(pd.Series(cluster1_names) + separator + pd.Series(cluster2_names)).values)

    return result


def counts_percent(counts: pd.Series,
                   threshold: float) -> int:
    total = len(counts)
    positive = len(counts[counts > 0])

    if (positive / total) > threshold:
        return 1
    else:
        return 0


def cluster_interaction_percent(cluster_interaction: tuple,
                                interaction: pd.Series,
                                clusters_percents: dict,
                                ) -> int:
    percent_cluster_receptors = clusters_percents[cluster_interaction[0]]
    percent_cluster_ligands = clusters_percents[cluster_interaction[1]]

    receptor = interaction['multidata_1_id']
    percent_receptor = percent_cluster_receptors.loc[receptor]
    ligand = interaction['multidata_2_id']
    percent_ligand = percent_cluster_ligands.loc[ligand]

    if percent_receptor and percent_ligand:
        interaction_percent = 1

    else:
        interaction_percent = 0

    return interaction_percent


def get_significant_means(mean_analysis: pd.DataFrame,
                          result_percent: pd.DataFrame) -> pd.DataFrame:
    significant_means = mean_analysis.values.copy()
    mask = result_percent == 0
    significant_means[mask] = np.nan
    return pd.DataFrame(significant_means,
                        index=mean_analysis.index,
                        columns=mean_analysis.columns)


def build_significant_means(mean_analysis: pd.DataFrame,
                            result_percent: pd.DataFrame) -> (pd.Series, pd.DataFrame):
    """
    Calculates the significant means and add rank (number of non empty entries divided by total entries)
    """
    significant_means = get_significant_means(mean_analysis, result_percent)
    significant_mean_rank = significant_means.count(axis=1)  # type: pd.Series
    number_of_clusters = len(significant_means.columns)
    significant_mean_rank = significant_mean_rank.apply(lambda rank: rank / number_of_clusters)
    significant_mean_rank = significant_mean_rank.round(3)
    significant_mean_rank.name = 'rank'
    return significant_mean_rank, significant_means
