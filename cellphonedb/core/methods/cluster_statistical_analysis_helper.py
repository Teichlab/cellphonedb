import itertools
from functools import partial
from multiprocessing.pool import Pool

import pandas as pd

from cellphonedb.core.methods.cluster_statistical_analysis_complex_method import cluster_interaction_mean, \
    counts_percent, \
    cluster_interaction_percent


def get_significant_means(real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame) -> pd.DataFrame:
    significant_means = real_mean_analysis.copy()
    min_significant_mean = 0.05
    for index, mean_analysis in real_mean_analysis.iterrows():
        for cluster_interaction in list(result_percent.columns):
            if result_percent.at[index, cluster_interaction] > min_significant_mean:
                significant_means.at[index, cluster_interaction] = pd.np.nan
    return significant_means


def shuffle_meta(meta: pd.DataFrame) -> pd.DataFrame:
    meta_copy = meta.copy()
    pd.np.random.shuffle(meta_copy['cell_type'])

    return meta_copy


def build_clusters(meta: pd.DataFrame, counts: pd.DataFrame) -> dict:
    cluster_names = meta['cell_type'].drop_duplicates().tolist()
    clusters = {'names': cluster_names, 'counts': {}, 'means': {}}

    cluster_counts = {}
    cluster_means = {}

    for cluster_name in cluster_names:
        cells = meta[meta['cell_type'] == cluster_name].index
        cluster_count = counts.loc[:, cells]
        cluster_counts[cluster_name] = cluster_count
        cluster_means[cluster_name] = cluster_count.apply(lambda count: count.mean(), axis=1)

    clusters['counts'] = cluster_counts
    clusters['means'] = cluster_means

    return clusters


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates()

    counts_filtered = counts.filter(genes, axis=0)

    return counts_filtered


def filter_empty_cluster_counts(counts: pd.DataFrame) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    if counts.empty:
        return counts

    filtered_counts = counts[counts.apply(lambda row: row.sum() > 0, axis=1)]
    return filtered_counts


def mean_pvalue_result_build(real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame,
                             interactions_data_result: pd.DataFrame) -> pd.DataFrame:
    mean_pvalue_result = pd.DataFrame(index=real_mean_analysis.index)
    for interaction_cluster in real_mean_analysis.columns.values:
        mean_pvalue_result[interaction_cluster] = real_mean_analysis[interaction_cluster].astype(str).str.cat(
            result_percent[interaction_cluster].astype(str), sep=' | ')

    mean_pvalue_result = pd.concat([interactions_data_result, mean_pvalue_result], axis=1, join='inner', sort=False)

    return mean_pvalue_result


def get_cluster_combinations(cluster_names):
    return sorted(itertools.product(cluster_names, repeat=2))


def build_result_matrix(interactions: pd.DataFrame, cluster_interactions: list) -> pd.DataFrame:
    columns = []

    for cluster_interaction in cluster_interactions:
        columns.append('{}_{}'.format(cluster_interaction[0], cluster_interaction[1]))

    result = pd.DataFrame(index=interactions.index, columns=columns, dtype=float)

    return result


def mean_analysis(interactions: pd.DataFrame, clusters: dict, cluster_interactions: list,
                  base_result: pd.DataFrame, suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    result = base_result.copy()

    for interaction_index, interaction in interactions.iterrows():
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{}_{}'.format(cluster_interaction[0], cluster_interaction[1])

            interaction_mean = cluster_interaction_mean(cluster_interaction, interaction, clusters['means'], suffixes)

            result.at[interaction_index, cluster_interaction_string] = interaction_mean

    return result


def percent_analysis(clusters: dict, threshold: float, interactions: pd.DataFrame, cluster_interactions: list,
                     base_result: pd.DataFrame, suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    result = base_result.copy()
    percents = {}
    for cluster_name in clusters['names']:
        counts = clusters['counts'][cluster_name]

        percents[cluster_name] = counts.apply(lambda count: counts_percent(count, threshold), axis=1)

    for interaction_index, interaction in interactions.iterrows():
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{}_{}'.format(cluster_interaction[0], cluster_interaction[1])

            interaction_percent = cluster_interaction_percent(cluster_interaction, interaction, percents, suffixes)
            result.at[interaction_index, cluster_interaction_string] = interaction_percent

    return result


def shuffled_analysis(iterations: int, meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame,
                      cluster_interactions: list, base_result: pd.DataFrame, threads: int,
                      suffixes: tuple = ('_1', '_2')) -> list:
    with Pool(processes=threads) as pool:
        asd_mult = partial(_statistical_analysis, base_result, cluster_interactions, counts, interactions, meta,
                           suffixes)
        results = pool.map(asd_mult, range(iterations))

    return results


def _statistical_analysis(base_result, cluster_interactions, counts, interactions, meta, suffixes,
                          iteration_number):
    shuffled_meta = shuffle_meta(meta)
    shuffled_clusters = build_clusters(shuffled_meta, counts)
    return mean_analysis(interactions, shuffled_clusters, cluster_interactions, base_result, suffixes)


def build_percent_result(real_mean_analysis: pd.DataFrame, real_perecents_analysis: pd.DataFrame,
                         statistical_mean_analysis: list, interactions: pd.DataFrame, cluster_interactions: list,
                         base_result: pd.DataFrame) -> pd.DataFrame:
    percent_result = base_result.copy()

    for interaction_index, interaction in interactions.iterrows():
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{}_{}'.format(cluster_interaction[0], cluster_interaction[1])
            real_mean = real_mean_analysis.at[interaction_index, cluster_interaction_string]
            real_percent = real_perecents_analysis.at[interaction_index, cluster_interaction_string]

            if int(real_percent) == 0 or real_mean == 0:
                result_percent = 1.0

            else:
                shuffled_bigger = 0

                for statistical_mean in statistical_mean_analysis:
                    mean = statistical_mean.at[interaction_index, cluster_interaction_string]
                    if mean > real_mean:
                        shuffled_bigger += 1

                result_percent = shuffled_bigger / len(statistical_mean_analysis)

            percent_result.at[interaction_index, cluster_interaction_string] = result_percent

    return percent_result


def interacting_pair_build(interactions: pd.DataFrame) -> pd.Series:
    def get_interactor_name(interaction: pd.Series, suffix: str) -> str:
        if interaction['is_complex{}'.format(suffix)]:
            return interaction['name{}'.format(suffix)]

        return interaction['gene_name{}'.format(suffix)]

    interacting_pair = interactions.apply(
        lambda interaction: '{}_{}'.format(get_interactor_name(interaction, '_1'),
                                           get_interactor_name(interaction, '_2')), axis=1)

    interacting_pair.rename('interacting_pair', inplace=True)

    return interacting_pair


def build_significant_means(real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame) -> (
        pd.Series, pd.DataFrame):
    significant_means = get_significant_means(real_mean_analysis, result_percent)
    significant_mean_rank = significant_means.count(axis=1)  # type: pd.Series
    number_of_clusters = len(significant_means.columns)
    significant_mean_rank = significant_mean_rank.apply(lambda rank: rank / number_of_clusters)
    significant_mean_rank = significant_mean_rank.round(3)
    significant_mean_rank.name = 'rank'
    return significant_mean_rank, significant_means
