from functools import partial

import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.exceptions.AllCountsFilteredException import AllCountsFilteredException
from cellphonedb.src.core.methods import cpdb_statistical_analysis_helper
from cellphonedb.src.core.models.cluster_counts import cluster_counts_helper, cluster_counts_filter
from cellphonedb.src.core.models.complex import complex_helper


def call(meta: pd.DataFrame,
         counts: pd.DataFrame,
         counts_data: str,
         interactions: pd.DataFrame,
         genes: pd.DataFrame,
         complexes: pd.DataFrame,
         complex_compositions: pd.DataFrame,
         pvalue: float,
         separator: str,
         iterations: int = 1000,
         threshold: float = 0.1,
         threads: int = 4,
         debug_seed: int = -1,
         result_precision: int = 3,
         ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info(
        '[Cluster Statistical Analysis Complex] '
        'Threshold:{} Iterations:{} Debug-seed:{} Threads:{} Precision:{}'.format(threshold,
                                                                                  iterations,
                                                                                  debug_seed,
                                                                                  threads,
                                                                                  result_precision))
    if debug_seed >= 0:
        pd.np.random.seed(debug_seed)
        core_logger.warning('Debug random seed enabled. Setted to {}'.format(debug_seed))

    cells_names = sorted(counts.columns)

    interactions_filtered, counts_filtered, complex_in_counts = prefilters(interactions, counts, genes, complexes,
                                                                           complex_compositions, counts_data)
    if interactions_filtered.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    complex_significative_protein = get_complex_significative(complex_in_counts, counts_filtered, complex_compositions,
                                                              cells_names)

    clusters = cpdb_statistical_analysis_helper.build_clusters(meta, counts_filtered)
    core_logger.info('Running Real Complex Analysis')

    cluster_interactions = cpdb_statistical_analysis_helper.get_cluster_combinations(clusters['names'])
    interactions_processed = get_interactions_processed(interactions_filtered, complex_significative_protein,
                                                        counts_data=counts_data)

    base_result = cpdb_statistical_analysis_helper.build_result_matrix(interactions_processed,
                                                                       cluster_interactions,
                                                                       separator)

    real_mean_analysis = cpdb_statistical_analysis_helper.mean_analysis(interactions_processed,
                                                                        clusters,
                                                                        cluster_interactions,
                                                                        base_result,
                                                                        separator,
                                                                        counts_data=counts_data)

    real_percents_analysis = cpdb_statistical_analysis_helper.percent_analysis(clusters,
                                                                               threshold,
                                                                               interactions_processed,
                                                                               cluster_interactions,
                                                                               base_result,
                                                                               separator,
                                                                               counts_data=counts_data)

    statistical_mean_analysis = cpdb_statistical_analysis_helper.shuffled_analysis(iterations,
                                                                                   meta,
                                                                                   counts_filtered,
                                                                                   interactions_processed,
                                                                                   cluster_interactions,
                                                                                   base_result,
                                                                                   threads,
                                                                                   separator,
                                                                                   counts_data=counts_data)

    result_percent = cpdb_statistical_analysis_helper.build_percent_result(real_mean_analysis,
                                                                           real_percents_analysis,
                                                                           statistical_mean_analysis,
                                                                           interactions_processed,
                                                                           cluster_interactions,
                                                                           base_result,
                                                                           separator)

    pvalues_result, means_result, significant_means, deconvoluted_result = build_results(
        interactions_filtered,
        real_mean_analysis,
        result_percent,
        clusters['means'],
        complex_compositions,
        counts,
        genes,
        result_precision,
        pvalue,
        counts_data
    )
    return pvalues_result, means_result, significant_means, deconvoluted_result


def build_results(interactions: pd.DataFrame,
                  real_mean_analysis: pd.DataFrame,
                  result_percent: pd.DataFrame,
                  clusters_means: dict,
                  complex_compositions: pd.DataFrame,
                  counts: pd.DataFrame,
                  genes: pd.DataFrame,
                  result_precision: int,
                  pvalue: float,
                  counts_data: str
                  ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
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

    significant_mean_rank, significant_means = cpdb_statistical_analysis_helper.build_significant_means(
        real_mean_analysis, result_percent, pvalue)
    significant_means = significant_means.round(result_precision)

    gene_columns = ['{}_{}'.format(counts_data, suffix) for suffix in ('1', '2')]
    gene_renames = {column: 'gene_{}'.format(suffix) for column, suffix in zip(gene_columns, ['a', 'b'])}

    # Remove useless columns
    interactions_data_result = pd.DataFrame(
        interactions[['id_cp_interaction', 'partner_a', 'partner_b', 'receptor_1', 'receptor_2', *gene_columns,
                      'annotation_strategy']].copy())

    interactions_data_result = pd.concat([interacting_pair, interactions_data_result], axis=1, sort=False)

    interactions_data_result['secreted'] = (interactions['secreted_1'] | interactions['secreted_2'])
    interactions_data_result['is_integrin'] = (interactions['integrin_1'] | interactions['integrin_2'])

    interactions_data_result.rename(
        columns={**gene_renames, 'receptor_1': 'receptor_a', 'receptor_2': 'receptor_b'},
        inplace=True)

    # Dedupe rows and filter only desired columns
    interactions_data_result.drop_duplicates(inplace=True)

    means_columns = ['id_cp_interaction', 'interacting_pair', 'partner_a', 'partner_b', 'gene_a', 'gene_b', 'secreted',
                     'receptor_a', 'receptor_b', 'annotation_strategy', 'is_integrin']

    interactions_data_result = interactions_data_result[means_columns]

    real_mean_analysis = real_mean_analysis.round(result_precision)
    significant_means = significant_means.round(result_precision)

    # Round result decimals
    for key, cluster_means in clusters_means.items():
        clusters_means[key] = cluster_means.round(result_precision)

    # Document 1
    pvalues_result = pd.concat([interactions_data_result, result_percent], axis=1, join='inner', sort=False)

    # Document 2
    means_result = pd.concat([interactions_data_result, real_mean_analysis], axis=1, join='inner', sort=False)

    # Document 3
    significant_means_result = pd.concat([interactions_data_result, significant_mean_rank, significant_means], axis=1,
                                         join='inner', sort=False)

    # Document 5
    deconvoluted_result = deconvoluted_complex_result_build(clusters_means, interactions, complex_compositions, counts,
                                                            genes, counts_data)

    return pvalues_result, means_result, significant_means_result, deconvoluted_result


def deconvoluted_complex_result_build(clusters_means: dict, interactions: pd.DataFrame,
                                      complex_compositions: pd.DataFrame, counts: pd.DataFrame,
                                      genes: pd.DataFrame, counts_data: str) -> pd.DataFrame:
    genes_counts = list(counts.index)
    genes_filtered = genes[genes[counts_data].apply(lambda gene: gene in genes_counts)]

    deconvoluted_complex_result_1 = deconvolute_complex_interaction_component(complex_compositions, genes_filtered,
                                                                              interactions, '_1', counts_data)
    deconvoluted_simple_result_1 = deconvolute_interaction_component(interactions, '_1', counts_data)

    deconvoluted_complex_result_2 = deconvolute_complex_interaction_component(complex_compositions, genes_filtered,
                                                                              interactions, '_2', counts_data)
    deconvoluted_simple_result_2 = deconvolute_interaction_component(interactions, '_2', counts_data)

    deconvoluted_result = deconvoluted_complex_result_1.append(
        [deconvoluted_simple_result_1, deconvoluted_complex_result_2, deconvoluted_simple_result_2], sort=False)

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


def deconvolute_interaction_component(interactions, suffix, counts_data):
    interactions = interactions[~interactions['is_complex{}'.format(suffix)]]
    deconvoluted_result = pd.DataFrame()
    deconvoluted_result['gene'] = interactions['{}{}'.format(counts_data, suffix)]

    deconvoluted_result[['protein_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction', 'receptor']] = \
        interactions[['protein_name{}'.format(suffix), 'gene_name{}'.format(suffix), 'name{}'.format(suffix),
                      'is_complex{}'.format(suffix), 'id_cp_interaction', 'receptor{}'.format(suffix)]]
    deconvoluted_result['complex_name'] = pd.np.nan

    return deconvoluted_result


def deconvolute_complex_interaction_component(complex_compositions, genes_filtered, interactions, suffix, counts_data):
    deconvoluted_result = pd.DataFrame()
    component = pd.DataFrame()
    component[counts_data] = interactions['{}{}'.format(counts_data, suffix)]
    component[['protein_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction', 'id_multidata', 'receptor']] = \
        interactions[
            ['protein_name{}'.format(suffix), 'gene_name{}'.format(suffix),
             'name{}'.format(suffix), 'is_complex{}'.format(suffix), 'id_cp_interaction',
             'id_multidata{}'.format(suffix), 'receptor{}'.format(suffix)]]

    deconvolution_complex = pd.merge(complex_compositions, component, left_on='complex_multidata_id',
                                     right_on='id_multidata')
    deconvolution_complex = pd.merge(deconvolution_complex, genes_filtered, left_on='protein_multidata_id',
                                     right_on='protein_multidata_id', suffixes=['_complex', '_simple'])

    deconvoluted_result['gene'] = deconvolution_complex['{}_simple'.format(counts_data)]

    deconvoluted_result[
        ['protein_name', 'gene_name', 'name', 'is_complex', 'id_cp_interaction', 'receptor', 'complex_name']] = \
        deconvolution_complex[
            ['protein_name_simple', 'gene_name_simple', 'name_simple',
             'is_complex_complex', 'id_cp_interaction', 'receptor_simple', 'name_complex']]

    return deconvoluted_result


def get_interactions_processed(interactions: pd.DataFrame, complex_significative_gene: pd.Series,
                               counts_data: str = 'ensembl') -> pd.DataFrame:
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

    def interaction_processed_builder(interaction: pd.Series, prefix: str) -> pd.Series:

        built = pd.Series()

        if interaction['is_complex_1']:
            built['{}_1'.format(prefix)] = complex_significative_gene[interaction['name_1']]
        else:
            built['{}_1'.format(prefix)] = interaction['{}_1'.format(prefix)]

        if interaction['is_complex_2']:
            built['{}_2'.format(prefix)] = complex_significative_gene[interaction['name_2']]
        else:
            built['{}_2'.format(prefix)] = interaction['{}_2'.format(prefix)]
        return built

    processed_interactions = interactions.apply(partial(interaction_processed_builder, prefix=counts_data), axis=1)

    return processed_interactions


# TODO: Needs refactor too slow
def filter_interactions_by_genes(interactions: pd.DataFrame, genes: list, counts_data: str = 'ensembl') -> pd.DataFrame:
    """
    Removes interactions if the ensembl is not in genes list. If is it a complex, don't check
    """

    def filter_by_non_complex_element(interaction: pd.Series) -> bool:
        if not interaction['is_complex_1']:
            if interaction['{}_1'.format(counts_data)] in genes:
                return True

        if not interaction['is_complex_2']:
            if interaction['{}_2'.format(counts_data)] in genes:
                return True

        return False

    interactions_filtered = interactions[interactions.apply(filter_by_non_complex_element, axis=1)]
    return interactions_filtered


def prefilters(interactions: pd.DataFrame, counts: pd.DataFrame, genes: pd.DataFrame, complexes: pd.DataFrame,
               complex_compositions: pd.DataFrame, counts_data: str):
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

    counts_multidata = cluster_counts_filter.filter_by_gene(counts, genes, counts_data=counts_data)

    if counts_multidata.empty:
        raise AllCountsFilteredException(hint='Are you using human data?')

    complex_in_counts, counts_multidata_complex = get_involved_complex_from_counts(counts_multidata, clusters_names,
                                                                                   complexes, complex_compositions)

    if complex_in_counts.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    interactions_filtered = filter_interactions_by_genes(interactions, counts['gene'].tolist(), counts_data=counts_data)

    interactions_filtered = filter_interactions_by_complexes(interactions_filtered, complex_in_counts)

    counts_simple = filter_counts_by_interactions(counts_multidata, interactions_filtered, counts_data=counts_data)

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
                                  suffixes: tuple = ('_1', '_2'), counts_data: str = 'ensembl') -> pd.DataFrame:
    """
    Removes counts if is not defined in interactions components
    """
    genes = interactions['{}{}'.format(counts_data, suffixes[0])].append(
        interactions['{}{}'.format(counts_data, suffixes[1])]).drop_duplicates().tolist()

    counts_filtered = filter_counts_by_genes(counts, genes)

    return counts_filtered
