import pandas as pd

from src.core.core_logger import core_logger
from src.core.methods import cpdb_statistical_analysis_helper
from src.core.models.cluster_counts import cluster_counts_helper, cluster_counts_filter
from src.core.models.complex import complex_helper


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, genes: pd.DataFrame,
         complexes: pd.DataFrame, complex_compositions: pd.DataFrame, iterations: int = 1000, threshold: float = 0.1,
         threads: int = 4, debug_seed=False, round_decimals: int = 1) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info(
        '[Cluster Statistical Analysis Complex] Threshold:{} Iterations:{} Debug-seed:{} Threads:{}'.format(
            threshold, iterations, debug_seed, threads))
    if debug_seed >= 0:
        pd.np.random.seed(debug_seed)
        core_logger.warning('Debug random seed enabled. Setted to {}'.format(debug_seed))

    cells_names = sorted(counts.columns)

    interactions_filtered, counts_filtered, complex_in_counts = prefilters(interactions, counts, genes, complexes,
                                                                           complex_compositions)
    if interactions_filtered.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    complex_significative_protein = get_complex_significative(complex_in_counts, counts_filtered, complex_compositions,
                                                              cells_names)

    clusters = cpdb_statistical_analysis_helper.build_clusters(meta, counts_filtered)
    core_logger.info('Running Real Complex Analysis')

    cluster_interactions = cpdb_statistical_analysis_helper.get_cluster_combinations(clusters['names'])
    interactions_processed = get_interactions_processed(interactions_filtered, complex_significative_protein)

    base_result = cpdb_statistical_analysis_helper.build_result_matrix(interactions_processed, cluster_interactions)

    real_mean_analysis = cpdb_statistical_analysis_helper.mean_analysis(interactions_processed, clusters,
                                                                        cluster_interactions, base_result)

    real_percents_analysis = cpdb_statistical_analysis_helper.percent_analysis(clusters, threshold,
                                                                               interactions_processed,
                                                                               cluster_interactions,
                                                                               base_result)

    statistical_mean_analysis = cpdb_statistical_analysis_helper.shuffled_analysis(iterations, meta, counts_filtered,
                                                                                   interactions_processed,
                                                                                   cluster_interactions, base_result,
                                                                                   threads)

    result_percent = cpdb_statistical_analysis_helper.build_percent_result(real_mean_analysis,
                                                                           real_percents_analysis,
                                                                           statistical_mean_analysis,
                                                                           interactions_processed,
                                                                           cluster_interactions, base_result)
    pvalues_result, means_result, significant_means, mean_pvalue_result, deconvoluted_result = build_results(
        interactions_filtered,
        real_mean_analysis,
        result_percent,
        clusters['means'],
        complex_compositions,
        counts,
        genes,
        round_decimals
    )
    return pvalues_result, means_result, significant_means, mean_pvalue_result, deconvoluted_result


def build_results(interactions: pd.DataFrame, real_mean_analysis: pd.DataFrame, result_percent: pd.DataFrame,
                  clusters_means: dict, complex_compositions: pd.DataFrame, counts: pd.DataFrame,
                  genes: pd.DataFrame, round_decimals: int) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Sets the results data structure from method generated data. Results documents are defined by specs.
    """
    core_logger.info('Building Complex results')
    interacting_pair = cpdb_statistical_analysis_helper.interacting_pair_build(interactions)

    interactions = interactions.copy()

    def simple_complex_indicator(interaction: pd.Series, suffix: str) -> str:
        """
        Add simple/complex prefixes to interaction components
        """
        if interaction['is_complex{}'.format(suffix)]:
            return 'complex:{}'.format(interaction['name{}'.format(suffix)])

        return 'simple:{}'.format(interaction['name{}'.format(suffix)])

    interactions['partner_a'] = interactions.apply(lambda interaction: simple_complex_indicator(interaction, '_1'),
                                                   axis=1)
    interactions['partner_b'] = interactions.apply(lambda interaction: simple_complex_indicator(interaction, '_2'),
                                                   axis=1)
    # Remove useless columns
    interactions_data_result = pd.DataFrame(interactions[
                                                ['id_cp_interaction', 'partner_a', 'partner_b', 'ensembl_1',
                                                 'ensembl_2', 'source']].copy())

    interactions_data_result = pd.concat([interacting_pair, interactions_data_result], axis=1, sort=False)

    interactions_data_result['secreted'] = (interactions['secretion_1'] | interactions['secretion_2'])
    interactions_data_result['is_integrin'] = (
            interactions['integrin_interaction_1'] | interactions['integrin_interaction_2'])

    interactions_data_result.rename(
        columns={'ensembl_1': 'ensembl_a', 'ensembl_2': 'ensembl_b'},
        inplace=True)

    significant_mean_rank, significant_means = cpdb_statistical_analysis_helper.build_significant_means(
        real_mean_analysis, result_percent)

    result_percent = result_percent.round(round_decimals)
    real_mean_analysis = real_mean_analysis.round(round_decimals)
    significant_means = significant_means.round(round_decimals)

    # Round result decimals
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
    mean_pvalue_result = cpdb_statistical_analysis_helper.mean_pvalue_result_build(real_mean_analysis,
                                                                                   result_percent,
                                                                                   interactions_data_result)

    # Document 5
    deconvoluted_result = deconvoluted_complex_result_build(clusters_means, interactions, complex_compositions, counts,
                                                            genes)

    return pvalues_result, means_result, significant_mean_result, mean_pvalue_result, deconvoluted_result


def deconvoluted_complex_result_build(clusters_means: dict, interactions: pd.DataFrame,
                                      complex_compositions: pd.DataFrame, counts: pd.DataFrame,
                                      genes: pd.DataFrame) -> pd.DataFrame:
    genes_counts = list(counts.index)
    genes_filtered = genes[genes['ensembl'].apply(lambda gene: gene in genes_counts)]

    deconvoluted_complex_result_1 = deconvolute_complex_interaction_component(complex_compositions, genes_filtered,
                                                                              interactions, '_1')
    deconvoluted_simple_result_1 = deconvolute_interaction_component(interactions, '_1')

    deconvoluted_complex_result_2 = deconvolute_complex_interaction_component(complex_compositions, genes_filtered,
                                                                              interactions, '_2')
    deconvoluted_simple_result_2 = deconvolute_interaction_component(interactions, '_2')

    deconvoluted_result = deconvoluted_complex_result_1.append(
        [deconvoluted_simple_result_1, deconvoluted_complex_result_2, deconvoluted_simple_result_2], sort=False)

    deconvoluted_result.set_index('ensembl', inplace=True)

    cluster_counts = pd.DataFrame(index=deconvoluted_result.index)

    for key, cluster_means in clusters_means.items():
        cluster_counts[key] = cluster_means

    cluster_counts = cluster_counts.reindex(sorted(cluster_counts.columns), axis=1)

    deconvoluted_result = pd.concat([deconvoluted_result, cluster_counts], axis=1, join='inner', sort=False)

    deconvoluted_result.reset_index(inplace=True)
    return deconvoluted_result


def deconvolute_interaction_component(interactions, suffix):
    interactions = interactions[~interactions['is_complex{}'.format(suffix)]]
    deconvoluted_result = pd.DataFrame()
    deconvoluted_result[
        ['ensembl', 'entry_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction']] = \
        interactions[
            ['ensembl{}'.format(suffix), 'entry_name{}'.format(suffix), 'gene_name{}'.format(suffix),
             'name{}'.format(suffix), 'is_complex{}'.format(suffix), 'id_cp_interaction']]

    return deconvoluted_result


def deconvolute_complex_interaction_component(complex_compositions, genes_filtered, interactions, suffix):
    deconvoluted_result = pd.DataFrame()
    component = pd.DataFrame()
    component[
        ['ensembl', 'entry_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction',
         'id_multidata']] = \
        interactions[
            ['ensembl{}'.format(suffix), 'entry_name{}'.format(suffix), 'gene_name{}'.format(suffix),
             'name{}'.format(suffix), 'is_complex{}'.format(suffix), 'id_cp_interaction',
             'id_multidata{}'.format(suffix)]]

    deconvolution_complex = pd.merge(complex_compositions, component, left_on='complex_multidata_id',
                                     right_on='id_multidata')
    deconvolution_complex = pd.merge(deconvolution_complex, genes_filtered, left_on='protein_multidata_id',
                                     right_on='protein_multidata_id', suffixes=['_complex', '_simple'])
    deconvoluted_result[
        ['ensembl', 'entry_name', 'gene_name', 'name', 'is_complex', 'complex_name', 'id_cp_interaction']] = \
        deconvolution_complex[['ensembl_simple', 'entry_name_simple', 'gene_name_simple', 'name_simple',
                               'is_complex_complex', 'name_complex', 'id_cp_interaction']]

    return deconvoluted_result


def get_interactions_processed(interactions: pd.DataFrame, complex_significative_gene: pd.Series) -> pd.DataFrame:
    """
    Returns a interaction dataframe [ensembl_1/ensembl_2] with complex data changed to complex_significative_gene.
    Interactions index don't changes

    EXAMPLE:
        INPUT:
        interactions
                ensembl_1   ensembl_2   name_1      name_2      is_complex_1    is_complex_2
        1       ensembla                uniprota    complex1    false           true
        2                   ensemblb    complex2    uniprotb    true            false
        3       ensemblc    ensembld    complex3    complex4    true            true

        complex_significative_gene

        name        ensembl
        complex1    ensemblw
        complex2    ensemblx
        complex3    ensembly
        complex4    ensemblz

        RESULT:

            ensembl_1   ensembl_2
        1   ensembla    ensemblw
        2   ensemblx    ensemblb
        3   ensembly    ensemblz
    """

    def interaction_processed_builder(interaction: pd.Series) -> pd.Series:

        built = pd.Series()

        if interaction['is_complex_1']:
            built['ensembl_1'] = complex_significative_gene[interaction['name_1']]
        else:
            built['ensembl_1'] = interaction['ensembl_1']

        if interaction['is_complex_2']:
            built['ensembl_2'] = complex_significative_gene[interaction['name_2']]
        else:
            built['ensembl_2'] = interaction['ensembl_2']

        return built

    processed_interactions = interactions.apply(interaction_processed_builder, axis=1)

    return processed_interactions


# TODO: Needs refactor too slow
def filter_interactions_by_genes(interactions: pd.DataFrame, genes: list) -> pd.DataFrame:
    """
    Removes interactions if the ensembl is not in genes list. If is it a complex, don't check
    """

    def filter_by_non_complex_element(interaction: pd.Series) -> bool:
        if not interaction['is_complex_1']:
            if interaction['ensembl_1'] in genes:
                return True

        if not interaction['is_complex_2']:
            if interaction['ensembl_2'] in genes:
                return True

        return False

    interactions_filtered = interactions[interactions.apply(filter_by_non_complex_element, axis=1)]
    return interactions_filtered


def prefilters(interactions: pd.DataFrame, counts: pd.DataFrame, genes: pd.DataFrame, complexes: pd.DataFrame,
               complex_compositions: pd.DataFrame):
    """
    - Finds the complex defined in counts and calculates their counts values
    - Remove interactions if the simple component ensembl is not in the counts list
    - Remove interactions if the complex component is not in the calculated complex list
    - Remove undefined simple counts
    - Merge simple filtered counts and calculated complex counts
    - Remove duplicated counts
    """
    core_logger.info('Running Complex Prefilters')
    clusters_names = sorted(counts.columns.values)
    counts['gene'] = counts.index

    counts_multidata = cluster_counts_filter.filter_by_gene(counts, genes)

    complex_in_counts, counts_multidata_complex = get_involved_complex_from_counts(counts_multidata, clusters_names,
                                                                                   complexes, complex_compositions)

    if complex_in_counts.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    interactions_filtered = filter_interactions_by_genes(interactions, counts['gene'].tolist())

    interactions_filtered = filter_interactions_by_complexes(interactions_filtered, complex_in_counts)

    counts_simple = filter_counts_by_interactions(counts_multidata, interactions_filtered)

    counts_filtered = counts_simple.append(counts_multidata_complex, sort=False)

    # TODO: we need to add it to method log
    counts_filtered.drop_duplicates(['gene'], inplace=True)

    counts_filtered.set_index(counts_filtered['gene'], inplace=True)

    return interactions_filtered, counts_filtered, complex_in_counts


def filter_interactions_by_complexes(interactions: pd.DataFrame, complexes: pd.DataFrame) -> pd.DataFrame:
    """
    Remove interactiontion if one of these components is not in complexes dataframe
    """
    complex_ids = complexes['complex_multidata_id'].tolist()

    interactions_filtered = interactions[interactions.apply(
        lambda interaction: (interaction['multidata_1_id'] in complex_ids) or
                            (interaction['multidata_2_id'] in complex_ids),
        axis=1)].copy()

    interactions_filtered.drop_duplicates('id_cp_interaction', inplace=True)

    return interactions_filtered


def filter_counts_by_genes(counts: pd.DataFrame, genes: list) -> pd.DataFrame:
    """
    remove count if is not defined in genes list
    """
    counts_filtered = counts[counts['gene'].apply(lambda gene: gene in genes)]

    return counts_filtered


def get_involved_complex_from_counts(multidatas_counts: pd.DataFrame, clusters_names: list,
                                     complex_expanded: pd.DataFrame, complex_composition: pd.DataFrame) -> (
        pd.DataFrame, pd.DataFrame):
    """
    Finds the complexes defined in counts and calculates the counts values
    """
    proteins_in_complexes = complex_composition['protein_multidata_id'].tolist()

    # Remove counts that can't be part of a complex
    multidatas_counts_filtered = multidatas_counts[
        multidatas_counts['id_multidata'].apply(lambda multidata: multidata in proteins_in_complexes)]

    # Find complexes with all components defined in counts
    complex_composition_counts = complex_helper.get_involved_complex_from_protein(multidatas_counts_filtered,
                                                                                  complex_expanded,
                                                                                  complex_composition,
                                                                                  drop_duplicates=False)

    if complex_composition_counts.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Remove counts that are not defined in selected complexes
    multidatas_counts_filtered = filter_counts_by_genes(multidatas_counts_filtered,
                                                        complex_composition_counts['gene'].tolist())

    # Set the counts value a complex count. This is the minimum value of the cell component
    complex_counts = cluster_counts_helper.merge_complex_counts(clusters_names, complex_composition_counts,
                                                                list(complex_expanded.columns.values))

    # Removes empty counts
    complex_counts = cluster_counts_filter.filter_empty_cluster_counts(complex_counts, clusters_names)

    complex_counts.drop(clusters_names, axis=1, inplace=True)

    return complex_counts, multidatas_counts_filtered


def get_complex_significative(complexes: pd.DataFrame, counts: pd.DataFrame, complex_composition: pd.DataFrame,
                              cells_names: list) -> pd.Series:
    """
    Returns a table with the most significant ensembl count for one complex.

    The most significative count is the lower mean of the components.



    """
    complex_composition_complexes = pd.merge(complexes, complex_composition, on='complex_multidata_id')

    complex_counts = pd.merge(counts, complex_composition_complexes, left_on='id_multidata',
                              right_on='protein_multidata_id', suffixes=('_protein', '_complex'))

    complex_more_significative_protein = pd.Series(data='', index=complex_counts['name_complex'].drop_duplicates())

    for _, complex in complexes.iterrows():
        complex_composition_proteins = complex_counts[complex_counts['id_complex'] == complex['id_complex']]

        means = pd.Series(index=complex_composition_proteins['gene'])

        for _, complex_composition_protein in complex_composition_proteins.iterrows():
            means[complex_composition_protein['gene']] = complex_composition_protein[cells_names].mean()

        min_mean = means.idxmin()

        complex_more_significative_protein.at[complex['name']] = min_mean

    return complex_more_significative_protein


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    """
    Removes counts if is not defined in interactions components
    """
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates().tolist()

    counts_filtered = filter_counts_by_genes(counts, genes)

    return counts_filtered
