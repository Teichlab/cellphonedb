import itertools

import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         debug_mode: bool = False) -> (pd.DataFrame, pd.DataFrame):
    # TODO: Check interactions with multiple genes
    interactions_filtered, counts_filtered = prefilters(counts, interactions)

    print(len(interactions_filtered))
    print(len(counts_filtered))

    clusters = build_clusters(meta, counts_filtered)
    cluster_interactions = get_cluster_combinations(clusters['names'])

    result_base = build_result_matrix(interactions_filtered, cluster_interactions)
    cluster_analysis(interactions_filtered, clusters, cluster_interactions, result_base.copy(deep=True))

    return (pd.DataFrame(), pd.DataFrame())


def cluster_analysis(interactions: pd.DataFrame, clusters: dict, cluster_interactions: list, means: pd.DataFrame):
    for interaction_index, interaction in interactions.iterrows():
        interaction_string = '{} - {}'.format(interaction['ensembl_receptor'], interaction['ensembl_ligand'])
        for cluster_interaction in cluster_interactions:
            cluster_interaction_string = '{} - {}'.format(cluster_interaction[0], cluster_interaction[1])

            counts_receptor = clusters['counts'][cluster_interaction[0]]
            counts_mean = clusters['means'][cluster_interaction[0]]

            mean_receptor = counts_mean[interaction['ensembl_receptor']]
            mean_ligand = counts_mean[interaction['ensembl_ligand']]

            if mean_receptor == 0 or mean_ligand == 0:
                interaction_mean = 0
            else:
                interaction_mean = (mean_receptor + mean_ligand) / 2

            print('means[{} - {}][{} - {}] = interaction_mean: {}'.format(interaction['ensembl_receptor'],
                                                                          interaction['ensembl_ligand'],
                                                                          cluster_interaction[0],
                                                                          cluster_interaction[1],
                                                                          interaction_mean))

            means.set_value(interaction_string, cluster_interaction_string, interaction_mean)

    return means


def build_result_matrix(interactions: pd.DataFrame, cluster_interactions: list) -> pd.DataFrame:
    columns = []
    indexes = []

    for cluster_interaction in cluster_interactions:
        columns.append('{} - {}'.format(cluster_interaction[0], cluster_interaction[1]))

    for index, interaction in interactions.iterrows():
        indexes.append('{} - {}'.format(interaction['ensembl_receptor'], interaction['ensembl_ligand']))

    result = pd.DataFrame(index=indexes, columns=columns)

    return result


def build_clusters(meta: pd.DataFrame, counts: pd.DataFrame) -> dict:
    cluster_names = meta['cell_type'].drop_duplicates().tolist()
    clusters = {'names': cluster_names, 'counts': {}, 'means': {}}

    cluster_counts = {}
    cluster_means = {}

    for cluster_name in cluster_names:
        cells = meta[meta['cell_type'] == cluster_name].index
        cluster_count = counts.loc[:, cells]
        cluster_counts[cluster_name] = cluster_count
        cluster_means[cluster_name] = cluster_count.apply(lambda counts: counts.mean(), axis=1)

    clusters['counts'] = cluster_counts
    clusters['means'] = cluster_means

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
