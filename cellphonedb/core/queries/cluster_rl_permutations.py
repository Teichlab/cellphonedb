import itertools

import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         debug_mode: bool = False, threshold: float = 0.3) -> (pd.DataFrame, pd.DataFrame):
    # TODO: Check interactions with multiple genes
    interactions_filtered, counts_filtered = prefilters(counts, interactions)

    print(len(interactions_filtered))
    print(len(counts_filtered))

    clusters = build_clusters(meta, counts_filtered, threshold)
    cluster_interactions = get_cluster_combinations(clusters['names'])

    base_result = build_result_matrix(interactions_filtered, cluster_interactions)

    real_result = {'means': base_result.copy(deep=True), 'percents': base_result.copy(deep=True)}
    real_result = cluster_analysis(interactions_filtered, clusters, cluster_interactions, real_result)

    shuffled_results = shuffled_cluster_analysis(iterations, threshold, meta, counts_filtered, interactions_filtered,
                                                 cluster_interactions,
                                                 base_result)

    result_percent = build_result(real_result, shuffled_results, interactions_filtered, cluster_interactions,
                                  base_result.copy(deep=True))
    return real_result['means'], result_percent


def build_result(real_result: dict, shuffled_results: list, interactions: pd.DataFrame, cluster_interactions: list,
                 base_result_percent: pd.DataFrame):
    for index, interaction in interactions.iterrows():
        interaction_string = '{} - {}'.format(interaction['ensembl_receptor'], interaction['ensembl_ligand'])
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{} - {}'.format(cluster_interaction[0], cluster_interaction[1])
            real_mean = real_result['means'].get_value(interaction_string, cluster_interaction_string)
            real_percent = real_result['percents'].get_value(interaction_string, cluster_interaction_string)
            print('{} - {} {} {}'.format(interaction_string, cluster_interaction_string, real_mean, real_percent))

            if real_percent == 0 or real_mean == 0:
                result_percent = 1

            else:
                shuffled_bigger = 0

                for shuffled_result in shuffled_results:
                    if (shuffled_result['means'].get_value(interaction_string, cluster_interaction_string) > real_mean):
                        shuffled_bigger += 1

                result_percent = shuffled_bigger / len(shuffled_results)

            base_result_percent.set_value(interaction_string, cluster_interaction_string, result_percent)

    return base_result_percent


def shuffled_cluster_analysis(iterations: int, threshold: float, meta: pd.DataFrame, counts: pd.DataFrame,
                              interactions: pd.DataFrame, cluster_interactions: list, base_result: pd.DataFrame):
    shuffled_results = []

    meta = meta.copy()
    for i in range(iterations):
        iteration_result = {'means': base_result.copy(deep=True), 'percents': base_result.copy(deep=True)}
        shuffle_meta(meta)
        shuffled_clusters = build_clusters(meta, counts, threshold)
        iteration_result = cluster_analysis(interactions, shuffled_clusters, cluster_interactions, iteration_result)

        shuffled_results.append(iteration_result)

    return shuffled_results


def shuffle_meta(meta: pd.DataFrame) -> pd.DataFrame:
    pd.np.random.shuffle(meta['cell_type'])

    return meta


def cluster_analysis(interactions: pd.DataFrame, clusters: dict, cluster_interactions: list, result: dict):
    for interaction_index, interaction in interactions.iterrows():
        interaction_string = '{} - {}'.format(interaction['ensembl_receptor'], interaction['ensembl_ligand'])
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{} - {}'.format(cluster_interaction[0], cluster_interaction[1])

            interaction_mean = cluster_interaction_mean(cluster_interaction, interaction, clusters['means'])
            interaction_percent = cluster_interaction_percent(cluster_interaction, interaction, clusters['percents'])

            result['means'].set_value(interaction_string, cluster_interaction_string, interaction_mean)
            result['percents'].set_value(interaction_string, cluster_interaction_string, interaction_percent)

    return result


def cluster_interaction_mean(cluster_interaction: tuple, interaction: pd.Series, clusters_means: dict) -> float:
    means_cluster_receptors = clusters_means[cluster_interaction[0]]
    means_cluster_ligands = clusters_means[cluster_interaction[1]]

    mean_receptor = means_cluster_receptors[interaction['ensembl_receptor']]
    mean_ligand = means_cluster_ligands[interaction['ensembl_ligand']]

    if mean_receptor == 0 or mean_ligand == 0:
        interaction_mean = 0
    else:
        interaction_mean = (mean_receptor + mean_ligand) / 2

    return interaction_mean


def cluster_interaction_percent(cluster_interaction: tuple, interaction: pd.Series, clusters_percents: dict) -> int:
    percent_cluster_receptors = clusters_percents[cluster_interaction[0]]
    percent_cluster_ligands = clusters_percents[cluster_interaction[1]]

    percent_receptor = percent_cluster_receptors[interaction['ensembl_receptor']]
    percent_ligand = percent_cluster_ligands[interaction['ensembl_ligand']]

    if percent_receptor == 0 or percent_ligand == 0:
        interaction_percent = 0

    else:
        interaction_percent = 1

    return interaction_percent


def build_result_matrix(interactions: pd.DataFrame, cluster_interactions: list) -> pd.DataFrame:
    columns = []
    indexes = []

    for cluster_interaction in cluster_interactions:
        columns.append('{} - {}'.format(cluster_interaction[0], cluster_interaction[1]))

    for index, interaction in interactions.iterrows():
        indexes.append('{} - {}'.format(interaction['ensembl_receptor'], interaction['ensembl_ligand']))

    result = pd.DataFrame(index=indexes, columns=columns)

    return result


def build_clusters(meta: pd.DataFrame, counts: pd.DataFrame, threshold: float) -> dict:
    cluster_names = meta['cell_type'].drop_duplicates().tolist()
    clusters = {'names': cluster_names, 'counts': {}, 'means': {}, 'percents': {}}

    cluster_counts = {}
    cluster_means = {}
    cluster_percent = {}

    for cluster_name in cluster_names:
        cells = meta[meta['cell_type'] == cluster_name].index
        cluster_count = counts.loc[:, cells]
        cluster_counts[cluster_name] = cluster_count
        cluster_means[cluster_name] = cluster_count.apply(lambda counts: counts.mean(), axis=1)

        def counts_percent(counts, threshold):
            total = len(counts)
            positive = len(counts[counts > 0])

            if positive / total < threshold:
                return 0
            else:
                return 1

        cluster_percent[cluster_name] = cluster_count.apply(lambda counts: counts_percent(counts, threshold),
                                                            axis=1)

    clusters['counts'] = cluster_counts
    clusters['means'] = cluster_means
    clusters['percents'] = cluster_percent

    return clusters


def prefilters(counts: pd.DataFrame, interactions: pd.DataFrame):
    interactions_filtered = filter_interaction.filter_by_receptor_ligand_ligand_receptor(interactions,
                                                                                         enable_integrin=False,
                                                                                         avoid_duplited=True)
    counts_filtered = filter_counts_by_interactions(counts, interactions)
    counts_filtered = filter_empty_cluster_counts(counts_filtered)
    interactions_filtered = filter_interactions_by_counts(interactions_filtered, counts_filtered,
                                                          ('_receptor', '_ligand'))
    interactions_filtered = filter_interactions_non_individual(interactions_filtered, ('_receptor', '_ligand'))

    # TODO: waiting for aproval. What happens when there are duplicated interactions (gene-gene)? Remove duplicates its a temp solution
    interactions_filtered = interactions_filtered[
        ~interactions_filtered.duplicated(['ensembl_receptor', 'ensembl_ligand'], keep='first')]

    counts_filtered = filter_counts_by_interactions(counts_filtered, interactions_filtered, ('_receptor', '_ligand'))

    return interactions_filtered, counts_filtered


def filter_empty_cluster_counts(counts: pd.DataFrame) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    if counts.empty:
        return counts

    filtered_counts = counts[counts.apply(lambda row: row.sum() > 0, axis=1)]
    return filtered_counts


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates()

    counts_filtered = counts.filter(genes, axis=0)

    return counts_filtered


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    ensembl_counts = counts.index
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
