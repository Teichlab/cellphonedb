import itertools

import pandas as pd

from cellphonedb.core.models.cluster_counts import helper_cluster_counts, filter_cluster_counts
from cellphonedb.core.models.complex import complex_helper
from cellphonedb.core.queries import cluster_rl_permutations


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, genes: pd.DataFrame,
         complexes: pd.DataFrame, complex_compositions: pd.DataFrame, iterations: int = 1000,
         debug_seed=False,
         threshold: float = 0.3, ) -> (pd.DataFrame, pd.DataFrame):
    if debug_seed is not False:
        pd.np.random.seed(debug_seed)

    cells_names = sorted(counts.columns)

    interactions_filtered, counts_filtered, complex_in_counts = prefilters(interactions, counts, genes, complexes,
                                                                           complex_compositions)

    complex_significative_protein = get_complex_significative(complex_in_counts, counts_filtered, complex_compositions,
                                                              cells_names)

    clusters = build_clusters(meta, counts_filtered)

    cluster_interactions = get_cluster_combinations(clusters['names'])
    interactions_processed = get_interactions_processed(interactions_filtered, complex_significative_protein)
    base_result = build_result_matrix(interactions_processed, cluster_interactions)

    real_mean_analysis = mean_analysis(interactions_processed, clusters, cluster_interactions, base_result)
    real_percernts_analysis = percent_analysis(clusters, threshold, interactions_processed, cluster_interactions,
                                               base_result)

    statistical_mean_analysis = shuffled_analysis(iterations, meta, counts_filtered, interactions_processed,
                                                  cluster_interactions, base_result)

    percent_result = build_percent_result(real_mean_analysis, real_percernts_analysis, statistical_mean_analysis,
                                          interactions_processed, cluster_interactions, base_result)

    return real_mean_analysis, percent_result


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
        shuffled_meta = cluster_rl_permutations.shuffle_meta(meta)
        shuffled_clusters = build_clusters(shuffled_meta, counts)
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

    interactions_filtered = filter_interactions_by_genes(interactions, counts['gene'].tolist())
    interactions_filtered = filter_interactions_by_complexes(interactions_filtered, complex_in_counts)

    counts_simple = filter_counts_by_interactions(counts_multidata, interactions_filtered)

    counts_filtered = counts_simple.append(counts_multidata_complex)

    counts_filtered.set_index(counts_filtered['gene'], inplace=True)

    # TODO: waiting for aproval. What happens when ensembl is duplicated? Remove duplicates its a temp solution
    counts_filtered.drop_duplicates('gene', inplace=True)

    return interactions_filtered, counts_filtered, complex_in_counts


def build_result_matrix(interactions: pd.DataFrame, cluster_interactions: list) -> pd.DataFrame:
    columns = []

    for cluster_interaction in cluster_interactions:
        columns.append('{}_{}'.format(cluster_interaction[0], cluster_interaction[1]))

    result = pd.DataFrame(index=interactions.index, columns=columns)

    return result


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


def filter_interactions_by_complexes(interactions: pd.DataFrame, complexes: pd.DataFrame) -> pd.DataFrame:
    complex_ids = complexes['complex_multidata_id'].tolist()

    interactions_filtered = interactions[interactions.apply(
        lambda interaction: (interaction['multidata_1_id'] in complex_ids) or
                            (interaction['multidata_2_id'] in complex_ids),
        axis=1)]

    interactions_filtered.drop_duplicates('id_interaction', inplace=True)

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
