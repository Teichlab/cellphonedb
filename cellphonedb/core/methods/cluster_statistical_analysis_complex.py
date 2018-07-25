import itertools

import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.models.cluster_counts import helper_cluster_counts, filter_cluster_counts
from cellphonedb.core.models.complex import complex_helper
from cellphonedb.core.methods import cluster_statistical_analysis_simple


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, genes: pd.DataFrame,
         complexes: pd.DataFrame, complex_compositions: pd.DataFrame, iterations: int = 1000, threshold: float = 0.1,
         debug_seed=False, round_decimals: int = 1) -> (
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    core_logger.info(
        '[Cluster Statistical Analysis Complex] Threshold: {} Debug-seed: {}'.format(threshold, debug_seed))

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

    clusters = cluster_statistical_analysis_simple.build_clusters(meta, counts_filtered)

    cluster_interactions = get_cluster_combinations(clusters['names'])
    interactions_processed = get_interactions_processed(interactions_filtered, complex_significative_protein)
    base_result = build_result_matrix(interactions_processed, cluster_interactions)

    real_mean_analysis = mean_analysis(interactions_processed, clusters, cluster_interactions, base_result)
    real_percernts_analysis = percent_analysis(clusters, threshold, interactions_processed, cluster_interactions,
                                               base_result)

    statistical_mean_analysis = shuffled_analysis(iterations, meta, counts_filtered, interactions_processed,
                                                  cluster_interactions, base_result)

    result_percent = build_percent_result(real_mean_analysis, real_percernts_analysis, statistical_mean_analysis,
                                          interactions_processed, cluster_interactions, base_result)

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
    interacting_pair = interacting_pair_build(interactions)

    interactions = interactions.copy()

    def simple_complex_indicator(interaction: pd.Series, suffix: str) -> str:
        if interaction['is_complex{}'.format(suffix)]:
            return 'complex:{}'.format(interaction['name{}'.format(suffix)])

        return 'simple:{}'.format(interaction['name{}'.format(suffix)])

    interactions['partner_a'] = interactions.apply(lambda interaction: simple_complex_indicator(interaction, '_1'),
                                                   axis=1)
    interactions['partner_b'] = interactions.apply(lambda interaction: simple_complex_indicator(interaction, '_2'),
                                                   axis=1)

    interactions_data_result = pd.DataFrame(interactions[
                                                ['id_cp_interaction', 'partner_a', 'partner_b', 'ensembl_1',
                                                 'ensembl_2', 'source']].copy())

    interactions_data_result = pd.concat([interacting_pair, interactions_data_result], axis=1)

    interactions_data_result['secreted'] = (interactions['secretion_1'] | interactions['secretion_2'])
    interactions_data_result['is_integrin'] = (
            interactions['integrin_interaction_1'] | interactions['integrin_interaction_2'])

    interactions_data_result.rename(
        columns={'ensembl_1': 'ensembl_a', 'ensembl_2': 'ensembl_b'},
        inplace=True)

    significant_means = cluster_statistical_analysis_simple.get_significant_means(real_mean_analysis, result_percent)

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
    mean_pvalue_result = cluster_statistical_analysis_simple.mean_pvalue_result_build(real_mean_analysis,
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
        [deconvoluted_simple_result_1, deconvoluted_complex_result_2, deconvoluted_simple_result_2])

    deconvoluted_result.set_index('ensembl', inplace=True)

    for key, cluster_means in clusters_means.items():
        deconvoluted_result[key] = cluster_means

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


def build_percent_result(real_mean_analysis: pd.DataFrame, real_perecents_analysis: pd.DataFrame,
                         statistical_mean_analysis: list, interactions: pd.DataFrame, cluster_interactions: list,
                         base_result: pd.DataFrame) -> pd.DataFrame:
    percent_result = base_result.copy()

    for interaction_index, interaction in interactions.iterrows():
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{}_{}'.format(cluster_interaction[0], cluster_interaction[1])
            real_mean = real_mean_analysis.get_value(interaction_index, cluster_interaction_string)
            real_percent = real_perecents_analysis.get_value(interaction_index, cluster_interaction_string)

            if int(real_percent) == 0 or real_mean == 0:
                result_percent = 1.0

            else:
                shuffled_bigger = 0

                for statistical_mean in statistical_mean_analysis:
                    mean = statistical_mean.get_value(interaction_index, cluster_interaction_string)
                    if mean > real_mean:
                        shuffled_bigger += 1

                result_percent = shuffled_bigger / len(statistical_mean_analysis)

            percent_result.set_value(interaction_index, cluster_interaction_string, result_percent)

    return percent_result


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
            result.set_value(interaction_index, cluster_interaction_string, interaction_percent)

    return result


def cluster_interaction_percent(cluster_interaction: tuple, interaction: pd.Series, clusters_percents: dict,
                                suffixes: tuple = ('_1', '_2')) -> int:
    percent_cluster_receptors = clusters_percents[cluster_interaction[0]]
    percent_cluster_ligands = clusters_percents[cluster_interaction[1]]

    percent_receptor = percent_cluster_receptors[interaction['ensembl{}'.format(suffixes[0])]]
    percent_ligand = percent_cluster_ligands[interaction['ensembl{}'.format(suffixes[1])]]

    if percent_receptor or percent_ligand:
        interaction_percent = 0

    else:
        interaction_percent = 1

    return interaction_percent


def counts_percent(counts: pd.Series, threshold: float) -> int:
    total = len(counts)
    positive = len(counts[counts > 0])

    if positive / total < threshold:
        return 1
    else:
        return 0


def shuffled_analysis(iterations: int, meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame,
                      cluster_interactions: list, base_result: pd.DataFrame, suffixes: tuple = ('_1', '_2')) -> list:
    results = []
    for i in range(iterations):
        shuffled_meta = cluster_statistical_analysis_simple.shuffle_meta(meta)
        shuffled_clusters = cluster_statistical_analysis_simple.build_clusters(shuffled_meta, counts)
        results.append(mean_analysis(interactions, shuffled_clusters, cluster_interactions, base_result, suffixes))

    return results


def get_interactions_processed(interactions: pd.DataFrame, complex_significative_gen: pd.Series) -> pd.DataFrame:
    def interaction_processed_builder(interaction: pd.Series) -> pd.Series:

        built = pd.Series()

        if interaction['is_complex_1']:
            built['ensembl_1'] = complex_significative_gen[interaction['name_1']]
        else:
            built['ensembl_1'] = interaction['ensembl_1']

        if interaction['is_complex_2']:
            built['ensembl_2'] = complex_significative_gen[interaction['name_2']]
        else:
            built['ensembl_2'] = interaction['ensembl_2']

        return built

    processed_interactions = interactions.apply(interaction_processed_builder, axis=1)

    return processed_interactions


def filter_interactions_by_genes(interactions: pd.DataFrame, genes: list) -> pd.DataFrame:
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
    clusters_names = sorted(counts.columns.values)
    counts['gene'] = counts.index

    counts_multidata = filter_cluster_counts.filter_by_gene(counts, genes)

    complex_in_counts, counts_multidata_complex = get_involved_complex_from_counts(counts_multidata, clusters_names,
                                                                                   complexes, complex_compositions)

    if complex_in_counts.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    interactions_filtered = filter_interactions_by_genes(interactions, counts['gene'].tolist())
    interactions_filtered = filter_interactions_by_complexes(interactions_filtered, complex_in_counts)

    counts_simple = filter_counts_by_interactions(counts_multidata, interactions_filtered)

    counts_filtered = counts_simple.append(counts_multidata_complex)

    # TODO: we need to add it to method log
    counts_filtered.drop_duplicates(['gene'], inplace=True)

    counts_filtered.set_index(counts_filtered['gene'], inplace=True)

    return interactions_filtered, counts_filtered, complex_in_counts


def build_result_matrix(interactions: pd.DataFrame, cluster_interactions: list) -> pd.DataFrame:
    columns = []

    for cluster_interaction in cluster_interactions:
        columns.append('{}_{}'.format(cluster_interaction[0], cluster_interaction[1]))

    result = pd.DataFrame(index=interactions.index, columns=columns, dtype=float)

    return result


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


def filter_interactions_by_complexes(interactions: pd.DataFrame, complexes: pd.DataFrame) -> pd.DataFrame:
    complex_ids = complexes['complex_multidata_id'].tolist()

    interactions_filtered = interactions[interactions.apply(
        lambda interaction: (interaction['multidata_1_id'] in complex_ids) or
                            (interaction['multidata_2_id'] in complex_ids),
        axis=1)]

    interactions_filtered.drop_duplicates('id_cp_interaction', inplace=True)

    return interactions_filtered


def filter_interactions_by_non_integrin(interactions: pd.DataFrame) -> pd.DataFrame:
    interactions_filtered = interactions[
        (interactions['integrin_interaction_1'] == False) & (interactions['integrin_interaction_2'] == False)]

    return interactions_filtered


def filter_counts_by_genes(counts: pd.DataFrame, genes: list) -> pd.DataFrame:
    counts_filtered = counts[counts['gene'].apply(lambda gene: gene in genes)]

    return counts_filtered


def get_involved_complex_from_counts(multidatas_counts: pd.DataFrame, clusters_names: list,
                                     complex_expanded: pd.DataFrame, complex_composition: pd.DataFrame) -> (
        pd.DataFrame, pd.DataFrame):
    proteins_in_complexes = complex_composition['protein_multidata_id'].tolist()

    multidatas_counts_filtered = multidatas_counts[
        multidatas_counts['id_multidata'].apply(lambda multidata: multidata in proteins_in_complexes)]

    complex_composition_counts = complex_helper.get_involved_complex_from_protein(multidatas_counts_filtered,
                                                                                  complex_expanded,
                                                                                  complex_composition,
                                                                                  drop_duplicates=False)

    if complex_composition_counts.empty:
        return pd.DataFrame(), pd.DataFrame()

    multidatas_counts_filtered = filter_counts_by_genes(multidatas_counts_filtered,
                                                        complex_composition_counts['gene'].tolist())

    complex_counts = helper_cluster_counts.merge_complex_cluster_counts(clusters_names, complex_composition_counts,
                                                                        list(complex_expanded.columns.values))

    complex_counts = helper_cluster_counts.complex_counts = helper_cluster_counts.filter_empty_cluster_counts(
        complex_counts, clusters_names)

    complex_counts.drop(clusters_names, axis=1, inplace=True)

    return complex_counts, multidatas_counts_filtered


def get_complex_significative(complexes: pd.DataFrame, counts: pd.DataFrame, complex_composition: pd.DataFrame,
                              cells_names: list) -> pd.Series:
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

        complex_more_significative_protein.set_value(complex['name'], min_mean)

    return complex_more_significative_protein


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates().tolist()

    counts_filtered = filter_counts_by_genes(counts, genes)

    return counts_filtered


def mean_analysis(interactions: pd.DataFrame, clusters: dict, cluster_interactions: list,
                  base_result: pd.DataFrame, suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    result = base_result.copy()

    for interaction_index, interaction in interactions.iterrows():
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{}_{}'.format(cluster_interaction[0], cluster_interaction[1])

            interaction_mean = cluster_interaction_mean(cluster_interaction, interaction, clusters['means'], suffixes)

            result.set_value(interaction_index, cluster_interaction_string, interaction_mean)

    return result


def cluster_interaction_mean(cluster_interaction: tuple, interaction: pd.Series, clusters_means: dict,
                             suffixes: tuple = ('_1', '_2')) -> float:
    means_cluster_receptors = clusters_means[cluster_interaction[0]]
    means_cluster_ligands = clusters_means[cluster_interaction[1]]

    mean_receptor = means_cluster_receptors[interaction['ensembl{}'.format(suffixes[0])]]
    mean_ligand = means_cluster_ligands[interaction['ensembl{}'.format(suffixes[1])]]

    if mean_receptor == 0 or mean_ligand == 0:
        interaction_mean = 0
    else:
        interaction_mean = (mean_receptor + mean_ligand) / 2

    return interaction_mean
