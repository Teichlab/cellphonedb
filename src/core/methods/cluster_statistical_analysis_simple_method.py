import pandas as pd

from src.core.methods import cluster_statistical_analysis_helper
from src.core.core_logger import core_logger
from src.core.models.interaction import interaction_filter


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         threshold: float = 0.1,
         threads: int = 4, debug_seed=False, round_decimals: int = 1) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info(
        '[Cluster Statistical Analysis Simple] Threshold:{} Iterations:{} Debug-seed:{} Threads:{}'.format(
            threshold, iterations, debug_seed, threads))

    if debug_seed >= 0:
        pd.np.random.seed(debug_seed)
        core_logger.warning('Debug random seed enabled. Setted to {}'.format(debug_seed))

    interactions_filtered, counts_filtered = prefilters(counts, interactions)

    clusters = cluster_statistical_analysis_helper.build_clusters(meta, counts_filtered)
    core_logger.info('Running Real Simple Analysis')
    cluster_interactions = cluster_statistical_analysis_helper.get_cluster_combinations(clusters['names'])

    base_result = cluster_statistical_analysis_helper.build_result_matrix(interactions_filtered, cluster_interactions)

    real_mean_analysis = cluster_statistical_analysis_helper.mean_analysis(interactions_filtered, clusters,
                                                                           cluster_interactions, base_result,
                                                                           suffixes=('_1', '_2'))

    real_percent_analysis = cluster_statistical_analysis_helper.percent_analysis(clusters, threshold,
                                                                                 interactions_filtered,
                                                                                 cluster_interactions, base_result,
                                                                                 suffixes=('_1', '_2'))

    statistical_mean_analysis = cluster_statistical_analysis_helper.shuffled_analysis(iterations, meta,
                                                                                      counts_filtered,
                                                                                      interactions_filtered,
                                                                                      cluster_interactions,
                                                                                      base_result,
                                                                                      threads,
                                                                                      suffixes=('_1', '_2'))

    result_percent = cluster_statistical_analysis_helper.build_percent_result(real_mean_analysis,
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
    core_logger.info('Building Simple results')
    interacting_pair = cluster_statistical_analysis_helper.interacting_pair_build(interactions)

    interactions_data_result = pd.DataFrame(interactions[['id_cp_interaction', 'name_1', 'name_2', 'ensembl_1',
                                                          'ensembl_2', 'source']].copy())

    interactions_data_result = pd.concat([interacting_pair, interactions_data_result], axis=1, sort=False)

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

    significant_mean_rank, significant_means = cluster_statistical_analysis_helper.build_significant_means(
        real_mean_analysis, result_percent)

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
    significant_mean_result = pd.concat([interactions_data_result, significant_mean_rank, significant_means], axis=1,
                                        join='inner', sort=False)

    # Document 4
    mean_pvalue_result = cluster_statistical_analysis_helper.mean_pvalue_result_build(real_mean_analysis,
                                                                                      result_percent,
                                                                                      interactions_data_result)

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

    cluster_counts = pd.DataFrame(index=deconvoluted_result.index)
    for key, cluster_means in clusters_means.items():
        cluster_counts[key] = cluster_means

    cluster_counts = cluster_counts.reindex(sorted(cluster_counts.columns), axis=1)

    deconvoluted_result = pd.concat([deconvoluted_result, cluster_counts], axis=1, join='inner', sort=False)

    deconvoluted_result.reset_index(inplace=True)
    return deconvoluted_result


def prefilters(counts: pd.DataFrame, interactions: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    This is where _counts_ input and interactions are filtrated. We remove
        - Duplicated ensembl: Keep the first.
        - If ensembl is not in CellPhoneDB interactions.
        - Empty counts: Remove counts if all row values are 0.
        - Interactions without two components in counts.
        - Orphan ensembls: if the ensembl is only on one interaction component

    """
    core_logger.info('Running Simple Prefilters')
    interactions_filtered = interaction_filter.filter_by_is_interactor(interactions)

    counts_filtered = counts[~counts.index.duplicated()]
    counts_filtered = cluster_statistical_analysis_helper.filter_counts_by_interactions(counts_filtered, interactions)
    counts_filtered = cluster_statistical_analysis_helper.filter_empty_cluster_counts(counts_filtered)
    interactions_filtered = filter_interactions_by_counts(interactions_filtered, counts_filtered, ('_1', '_2'))

    counts_filtered = cluster_statistical_analysis_helper.filter_counts_by_interactions(counts_filtered,
                                                                                        interactions_filtered,
                                                                                        ('_1', '_2'))

    interactions_filtered.reset_index(inplace=True, drop=True)

    return interactions_filtered, counts_filtered


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    """
    Remove interaction if both components are not in counts lists
    """
    ensembl_counts = list(counts.index)
    interactions_filtered = interactions[interactions.apply(
        lambda row: row['ensembl{}'.format(suffixes[0])] in ensembl_counts and row[
            'ensembl{}'.format(suffixes[1])] in ensembl_counts, axis=1
    )]
    return interactions_filtered
