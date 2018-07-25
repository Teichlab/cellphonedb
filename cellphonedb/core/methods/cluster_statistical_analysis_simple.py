import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.models.interaction import filter_interaction
from cellphonedb.core.methods import cluster_statistical_analysis_complex


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         threshold: float = 0.1, debug_seed=False, round_decimals: int = 1) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info('[Cluster Statistical Analysis Simple] Threshold: {} Debug-seed: {}'.format(threshold, debug_seed))

    if debug_seed >= 0:
        pd.np.random.seed(debug_seed)
        core_logger.warning('Debug random seed enabled. Setted to {}'.format(debug_seed))

    interactions_filtered, counts_filtered = prefilters(counts, interactions)

    clusters = build_clusters(meta, counts_filtered)
    cluster_interactions = cluster_statistical_analysis_complex.get_cluster_combinations(clusters['names'])

    base_result = cluster_statistical_analysis_complex.build_result_matrix(interactions_filtered, cluster_interactions)

    real_mean_analysis = cluster_statistical_analysis_complex.mean_analysis(interactions_filtered, clusters,
                                                                            cluster_interactions, base_result,
                                                                            suffixes=('_1', '_2'))

    real_percent_analysis = cluster_statistical_analysis_complex.percent_analysis(clusters, threshold,
                                                                                  interactions_filtered,
                                                                                  cluster_interactions, base_result,
                                                                                  suffixes=('_1', '_2'))

    statistical_mean_analysis = cluster_statistical_analysis_complex.shuffled_analysis(iterations, meta,
                                                                                       counts_filtered,
                                                                                       interactions_filtered,
                                                                                       cluster_interactions,
                                                                                       base_result,
                                                                                       suffixes=('_1', '_2'))

    result_percent = cluster_statistical_analysis_complex.build_percent_result(real_mean_analysis,
                                                                               real_percent_analysis,
                                                                               statistical_mean_analysis,
                                                                               interactions_filtered,
                                                                               cluster_interactions, base_result)

    pvalues_result, means_result, significant_means, mean_pvalue_result, deconvoluted_result = build_results(
        interactions_filtered,
        real_mean_analysis,
        result_percent,
        clusters['means'],
        round_decimals)

    return pvalues_result, means_result, significant_means, mean_pvalue_result, deconvoluted_result


def build_results(interactions: pd.DataFrame, real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame,
                  clusters_means: dict, round_decimals: int) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    interacting_pair = cluster_statistical_analysis_complex.interacting_pair_build(interactions)

    interactions_data_result = pd.DataFrame(interactions[['id_cp_interaction', 'name_1', 'name_2', 'ensembl_1',
                                                          'ensembl_2', 'source']].copy())

    interactions_data_result = pd.concat([interacting_pair, interactions_data_result], axis=1)

    interactions_data_result['secreted'] = (interactions['secretion_1'] | interactions['secretion_2'])
    interactions_data_result['is_integrin'] = (
            interactions['integrin_interaction_1'] | interactions['integrin_interaction_2'])

    interactions_data_result.rename(
        columns={'name_1': 'partner_a', 'name_2': 'partner_b', 'ensembl_1': 'ensembl_a', 'ensembl_2': 'ensembl_b'},
        inplace=True)

    interactions_data_result['partner_a'] = interactions_data_result['partner_a'].apply(
        lambda name: 'simple:{}'.format(name))
    interactions_data_result['partner_b'] = interactions_data_result['partner_b'].apply(
        lambda name: 'simple:{}'.format(name))

    significant_means = get_significant_means(real_mean_analysis, result_percent)

    result_percent = result_percent.round(round_decimals)
    real_mean_analysis = real_mean_analysis.round(round_decimals)
    significant_means = significant_means.round(round_decimals)
    for key, cluster_means in clusters_means.items():
        clusters_means[key] = cluster_means.round(round_decimals)

    # Document 1
    pvalues_result = pd.concat([interactions_data_result, result_percent], axis=1, join='inner', sort=False)

    # Document 2
    means_result = pd.concat([interactions_data_result, real_mean_analysis], axis=1, join='inner', sort=False)

    # Document 3
    significant_mean_result = pd.concat([interactions_data_result, significant_means], axis=1, join='inner', sort=False)

    # Document 4
    mean_pvalue_result = mean_pvalue_result_build(real_mean_analysis, result_percent, interactions_data_result)

    # Document 5
    deconvoluted_result = deconvoluted_result_build(clusters_means, interactions)

    return pvalues_result, means_result, significant_mean_result, mean_pvalue_result, deconvoluted_result


def deconvoluted_result_build(clusters_means: dict, interactions: pd.DataFrame) -> pd.DataFrame:
    deconvoluted_result_1 = pd.DataFrame()
    deconvoluted_result_2 = pd.DataFrame()
    deconvoluted_result_1[
        ['ensembl', 'entry_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction']] = \
        interactions[
            ['ensembl_1', 'entry_name_1', 'gene_name_1', 'name_1', 'is_complex_1', 'id_cp_interaction']]
    deconvoluted_result_2[
        ['ensembl', 'entry_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction']] = \
        interactions[
            ['ensembl_2', 'entry_name_2', 'gene_name_2', 'name_2', 'is_complex_2', 'id_cp_interaction']]

    deconvoluted_result = deconvoluted_result_1.append(deconvoluted_result_2)

    deconvoluted_result.set_index('ensembl', inplace=True)

    for key, cluster_means in clusters_means.items():
        deconvoluted_result[key] = cluster_means

    deconvoluted_result.reset_index(inplace=True)
    return deconvoluted_result


def mean_pvalue_result_build(real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame,
                             interactions_data_result: pd.DataFrame) -> pd.DataFrame:
    mean_pvalue_result = pd.DataFrame(index=real_mean_analysis.index)
    for interaction_cluster in real_mean_analysis.columns.values:
        mean_pvalue_result[interaction_cluster] = real_mean_analysis[interaction_cluster].astype(str).str.cat(
            result_percent[interaction_cluster].astype(str), sep=' | ')

    mean_pvalue_result = pd.concat([interactions_data_result, mean_pvalue_result], axis=1, join='inner', sort=False)

    return mean_pvalue_result


def significament_mean_build(interactions_data_result: pd.DataFrame, real_mean_analysis: pd.DataFrame,
                             result_percent: pd.DataFrame) -> pd.DataFrame:
    pvalues_means_result = pd.concat([interactions_data_result, real_mean_analysis], axis=1, join='inner', sort=False)
    min_significant_mean = 0.05
    for index, mean_analysis in real_mean_analysis.iterrows():
        for cluster_interaction in list(result_percent.columns):
            if result_percent.get_value(index, cluster_interaction) > min_significant_mean:
                pvalues_means_result.set_value(index, cluster_interaction, pd.np.nan)
    return pvalues_means_result


def get_significant_means(real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame) -> pd.DataFrame:
    significant_means = real_mean_analysis.copy()
    min_significant_mean = 0.05
    for index, mean_analysis in real_mean_analysis.iterrows():
        for cluster_interaction in list(result_percent.columns):
            if result_percent.get_value(index, cluster_interaction) > min_significant_mean:
                significant_means.set_value(index, cluster_interaction, pd.np.nan)
    return significant_means


def shuffle_meta(meta: pd.DataFrame) -> pd.DataFrame:
    pd.np.random.shuffle(meta['cell_type'])

    return meta


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


def prefilters(counts: pd.DataFrame, interactions: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    interactions_filtered = filter_interaction.filter_by_is_interactor(interactions)

    counts_filtered = counts[~counts.index.duplicated()]
    counts_filtered = filter_counts_by_interactions(counts_filtered, interactions)
    counts_filtered = filter_empty_cluster_counts(counts_filtered)
    interactions_filtered = filter_interactions_by_counts(interactions_filtered, counts_filtered, ('_1', '_2'))
    interactions_filtered = filter_interactions_non_individual(interactions_filtered, ('_1', '_2'))

    counts_filtered = filter_counts_by_interactions(counts_filtered, interactions_filtered, ('_1', '_2'))

    interactions_filtered.reset_index(inplace=True, drop=True)

    return interactions_filtered, counts_filtered


def filter_empty_cluster_counts(counts: pd.DataFrame) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    if counts.empty:
        return counts

    filtered_counts = counts[counts.apply(lambda row: row.sum() > 0, axis=1)]
    return filtered_counts


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates()

    counts_filtered = counts.filter(genes, axis=0)

    return counts_filtered


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    ensembl_counts = list(counts.index)
    interactions_filtered = interactions[interactions.apply(
        lambda row: row['ensembl{}'.format(suffixes[0])] in ensembl_counts and row[
            'ensembl{}'.format(suffixes[1])] in ensembl_counts, axis=1
    )]
    return interactions_filtered


def filter_interactions_non_individual(interactions: pd.DataFrame, suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    interactions_filtered = interactions[
        interactions.apply(lambda interaction: interaction['ensembl{}'.format(suffixes[0])] != interaction[
            'ensembl{}'.format(suffixes[1])], axis=1)]

    return interactions_filtered
