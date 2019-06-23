import pandas as pd


def percent_analysis(clusters: dict,
                     threshold: float,
                     interactions: pd.DataFrame,
                     cluster_interactions: list,
                     base_result: pd.DataFrame,
                     separator: str,
                     suffixes: tuple = ('_1', '_2'),
                     counts_data: str = 'ensembl') -> pd.DataFrame:
    result = base_result.copy()
    percents = {}
    for cluster_name in clusters['names']:
        counts = clusters['counts'][cluster_name]

        percents[cluster_name] = counts.apply(lambda count: counts_percent(count, threshold), axis=1)

    for interaction_index, interaction in interactions.iterrows():
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{}{}{}'.format(cluster_interaction[0], separator, cluster_interaction[1])

            interaction_percent = cluster_interaction_percent(cluster_interaction, interaction, percents, suffixes,
                                                              counts_data=counts_data)

            result.at[interaction_index, cluster_interaction_string] = interaction_percent

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
                                suffixes: tuple = ('_1', '_2'),
                                counts_data: str = 'ensembl'
                                ) -> int:
    percent_cluster_receptors = clusters_percents[cluster_interaction[0]]
    percent_cluster_ligands = clusters_percents[cluster_interaction[1]]

    percent_receptor = percent_cluster_receptors[interaction['{}{}'.format(counts_data, suffixes[0])]]
    percent_ligand = percent_cluster_ligands[interaction['{}{}'.format(counts_data, suffixes[1])]]

    if percent_receptor and percent_ligand:
        interaction_percent = 1

    else:
        interaction_percent = 0

    return interaction_percent


def get_significant_means(mean_analysis: pd.DataFrame,
                          result_percent: pd.DataFrame) -> pd.DataFrame:
    significant_means = mean_analysis.copy()
    for index, mean_analysis in mean_analysis.iterrows():
        for cluster_interaction in list(result_percent.columns):
            if not result_percent.at[index, cluster_interaction]:
                significant_means.at[index, cluster_interaction] = pd.np.nan
    return significant_means


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
