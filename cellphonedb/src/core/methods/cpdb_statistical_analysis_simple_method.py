import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.methods import cpdb_statistical_analysis_helper


def call(meta: pd.DataFrame,
         counts: pd.DataFrame,
         counts_data: str,
         interactions: pd.DataFrame,
         pvalue: float,
         separator: str,
         iterations: int = 1000,
         threshold: float = 0.1,
         threads: int = 4,
         debug_seed: int = -1,
         result_precision: int = 3,
         ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info(
        '[Cluster Statistical Analysis Simple] '
        'Threshold:{} Iterations:{} Debug-seed:{} Threads:{} Precision:{}'.format(threshold,
                                                                                  iterations,
                                                                                  debug_seed,
                                                                                  threads,
                                                                                  result_precision))

    if debug_seed >= 0:
        pd.np.random.seed(debug_seed)
        core_logger.warning('Debug random seed enabled. Setted to {}'.format(debug_seed))

    interactions_filtered, counts_filtered = prefilters(counts, interactions, counts_data)

    if interactions_filtered.empty or counts_filtered.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    clusters = cpdb_statistical_analysis_helper.build_clusters(meta, counts_filtered)
    core_logger.info('Running Real Simple Analysis')
    cluster_interactions = cpdb_statistical_analysis_helper.get_cluster_combinations(clusters['names'])

    base_result = cpdb_statistical_analysis_helper.build_result_matrix(interactions_filtered,
                                                                       cluster_interactions,
                                                                       separator)

    real_mean_analysis = cpdb_statistical_analysis_helper.mean_analysis(interactions_filtered,
                                                                        clusters,
                                                                        cluster_interactions,
                                                                        base_result,
                                                                        separator,
                                                                        suffixes=('_1', '_2'),
                                                                        counts_data=counts_data)

    real_percent_analysis = cpdb_statistical_analysis_helper.percent_analysis(clusters,
                                                                              threshold,
                                                                              interactions_filtered,
                                                                              cluster_interactions,
                                                                              base_result,
                                                                              separator,
                                                                              suffixes=('_1', '_2'),
                                                                              counts_data=counts_data)

    statistical_mean_analysis = cpdb_statistical_analysis_helper.shuffled_analysis(iterations, meta,
                                                                                   counts_filtered,
                                                                                   interactions_filtered,
                                                                                   cluster_interactions,
                                                                                   base_result,
                                                                                   threads,
                                                                                   separator,
                                                                                   suffixes=('_1', '_2'),
                                                                                   counts_data=counts_data)

    result_percent = cpdb_statistical_analysis_helper.build_percent_result(real_mean_analysis,
                                                                           real_percent_analysis,
                                                                           statistical_mean_analysis,
                                                                           interactions_filtered,
                                                                           cluster_interactions,
                                                                           base_result,
                                                                           separator)

    pvalues_result, means_result, significant_means, deconvoluted_result = build_results(
        interactions_filtered,
        real_mean_analysis,
        result_percent,
        clusters['means'],
        result_precision,
        pvalue,
        counts_data
    )

    return pvalues_result, means_result, significant_means, deconvoluted_result


def build_results(interactions: pd.DataFrame,
                  real_mean_analysis: pd.DataFrame,
                  result_percent: pd.DataFrame,
                  clusters_means: dict,
                  result_precision: int,
                  pvalue: float,
                  counts_data: str,
                  ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info('Building Simple results')
    interacting_pair = cpdb_statistical_analysis_helper.interacting_pair_build(interactions)

    gene_columns = ['{}_{}'.format(counts_data, suffix) for suffix in ('1', '2')]
    gene_renames = {column: 'gene_{}'.format(suffix) for column, suffix in zip(gene_columns, ['a', 'b'])}

    interactions_data_result = pd.DataFrame(
        interactions[
            ['id_cp_interaction', 'name_1', 'name_2', 'receptor_1', 'receptor_2', *gene_columns, 'annotation_strategy']].copy())

    interactions_data_result = pd.concat([interacting_pair, interactions_data_result], axis=1, sort=False)

    interactions_data_result['secreted'] = (interactions['secreted_1'] | interactions['secreted_2'])
    interactions_data_result['is_integrin'] = (
            interactions['integrin_1'] | interactions['integrin_2'])

    interactions_data_result.rename(
        columns={'name_1': 'partner_a', 'name_2': 'partner_b', 'receptor_1': 'receptor_a', 'receptor_2': 'receptor_b',
                 **gene_renames},
        inplace=True)

    interactions_data_result['partner_a'] = interactions_data_result['partner_a'].apply(
        lambda name: 'simple:{}'.format(name))
    interactions_data_result['partner_b'] = interactions_data_result['partner_b'].apply(
        lambda name: 'simple:{}'.format(name))

    # Dedupe rows and filter only desired columns
    interactions_data_result.drop_duplicates(inplace=True)

    means_columns = ['id_cp_interaction', 'interacting_pair', 'partner_a', 'partner_b', 'gene_a', 'gene_b', 'secreted',
                     'receptor_a', 'receptor_b', 'annotation_strategy', 'is_integrin']

    interactions_data_result = interactions_data_result[means_columns]

    significant_mean_rank, significant_means = cpdb_statistical_analysis_helper.build_significant_means(
        real_mean_analysis, result_percent, pvalue)

    result_percent = result_percent.round(result_precision)
    real_mean_analysis = real_mean_analysis.round(result_precision)
    significant_means = significant_means.round(result_precision)
    for key, cluster_means in clusters_means.items():
        clusters_means[key] = cluster_means.round(result_precision)

    # Document 1
    pvalues_result = pd.concat([interactions_data_result, result_percent], axis=1, join='inner', sort=False)

    # Document 2
    means_result = pd.concat([interactions_data_result, real_mean_analysis], axis=1, join='inner', sort=False)

    # Document 3
    significant_mean_result = pd.concat([interactions_data_result, significant_mean_rank, significant_means], axis=1,
                                        join='inner', sort=False)

    # Document 5
    deconvoluted_result = deconvoluted_result_build(clusters_means, interactions, counts_data=counts_data)

    return pvalues_result, means_result, significant_mean_result, deconvoluted_result


def deconvoluted_result_build(clusters_means: dict, interactions: pd.DataFrame, counts_data: str) -> pd.DataFrame:
    deconvoluted_result_1 = pd.DataFrame()
    deconvoluted_result_2 = pd.DataFrame()
    deconvoluted_result_1['gene'] = interactions['{}_1'.format(counts_data)]
    deconvoluted_result_2['gene'] = interactions['{}_2'.format(counts_data)]

    deconvoluted_result_1[['protein_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction', 'receptor']] = \
        interactions[['protein_name_1', 'gene_name_1', 'name_1', 'is_complex_1', 'id_cp_interaction', 'receptor_1']]
    deconvoluted_result_2[['protein_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction', 'receptor']] = \
        interactions[['protein_name_2', 'gene_name_2', 'name_2', 'is_complex_2', 'id_cp_interaction', 'receptor_2']]

    deconvoluted_result = deconvoluted_result_1.append(deconvoluted_result_2)
    deconvoluted_result['complex_name'] = pd.np.nan

    deconvoluted_result.set_index('gene', inplace=True)

    cluster_counts = pd.DataFrame(index=deconvoluted_result.index)
    for key, cluster_means in clusters_means.items():
        cluster_counts[key] = cluster_means

    cluster_counts = cluster_counts.reindex(sorted(cluster_counts.columns), axis=1)

    # Here we sort and filter unwanted columns
    deconvoluted_columns = ['gene_name', 'name', 'is_complex', 'protein_name', 'complex_name', 'id_cp_interaction']

    deconvoluted_result = deconvoluted_result[deconvoluted_columns]
    deconvoluted_result.rename({'name': 'uniprot'}, axis=1, inplace=True)

    deconvoluted_result = pd.concat([deconvoluted_result, cluster_counts], axis=1, join='inner', sort=False)

    deconvoluted_result.reset_index(inplace=True)
    deconvoluted_result.drop(columns='gene', inplace=True)

    return deconvoluted_result


def prefilters(counts: pd.DataFrame, interactions: pd.DataFrame, counts_data: str) -> (pd.DataFrame, pd.DataFrame):
    """
    This is where _counts_ input and interactions are filtrated. We remove
        - Duplicated ensembl: Keep the first.
        - If ensembl is not in CellPhoneDB interactions.
        - Empty counts: Remove counts if all row values are 0.
        - Interactions without two components in counts.
        - Orphan ensembls: if the ensembl is only on one interaction component

    """
    core_logger.info('Running Simple Prefilters')

    counts_filtered = counts[~counts.index.duplicated()]
    counts_filtered = cpdb_statistical_analysis_helper.filter_counts_by_interactions(counts_filtered,
                                                                                     interactions,
                                                                                     counts_data=counts_data)
    counts_filtered = cpdb_statistical_analysis_helper.filter_empty_cluster_counts(counts_filtered)
    interactions_filtered = cpdb_statistical_analysis_helper.filter_interactions_by_counts(interactions,
                                                                                           counts_filtered,
                                                                                           ('_1', '_2'),
                                                                                           counts_data=counts_data)

    counts_filtered = cpdb_statistical_analysis_helper.filter_counts_by_interactions(counts_filtered,
                                                                                     interactions_filtered,
                                                                                     ('_1', '_2'),
                                                                                     counts_data=counts_data)

    interactions_filtered.reset_index(inplace=True, drop=True)

    return interactions_filtered, counts_filtered
