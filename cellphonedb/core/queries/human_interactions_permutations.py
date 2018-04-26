import pandas as pd

import collections
import numpy as np

from methods.one_one_human_interactions_permutations import one_one_human_interactions_permutations, \
    one_one_human_individual


# TODO: WIP
def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         start_interaction: int = 0, how_many: int = None, debug_mode: bool = False) -> (pd.DataFrame, pd.DataFrame):
    if debug_mode:
        np.random.seed(0)

    interactions = filter_interactions_by_receptor_ligand(interactions)
    interactions = filter_interactions_by_counts(interactions, counts)
    all_interactions = interactions.sort_values('id_interaction')

    # TODO: Remove
    if how_many:
        interactions = filter_interactions_by_range(start_interaction, how_many, all_interactions)

    counts_filtered = filter_counts_by_genes(interactions, counts)
    interactions = filter_interactions_by_counts(interactions, counts)
    interactions = filter_non_individual_interactions(interactions)
    counts_filtered = filter_counts_by_interactions(counts_filtered, interactions)
    cluster_names = meta.cell_type.unique()
    clusters_data = cells_to_clusters(cluster_names, meta, counts_filtered)
    all_clusters = clusters_data[0]
    clusters_counts = clusters_data[1]
    cluster_pairs = get_cluster_combinations(cluster_names)
    cells_values = meta['cell_type']
    cells_keys = meta.index
    cells_clusters = dict(zip(cells_keys, cells_values))
    all_pairs_means = collections.defaultdict(dict)

    for count_r in range(0, iterations + 1):
        clusters_values = sorted(cells_clusters.values())
        np.random.shuffle(clusters_values)

        new_meta = pd.DataFrame(
            {'Cell': sorted(cells_clusters.keys()),
             'cell_type': clusters_values
             })

        new_meta.set_index('Cell', inplace=True)

        clusters_data_shuffle = cells_to_clusters(cluster_names, new_meta, counts_filtered)
        all_clusters_shuffle = clusters_data_shuffle[0]
        clusters_means_shuffle = clusters_data_shuffle[2]

        one_one_human_interactions_permutations(interactions, all_clusters_shuffle, clusters_means_shuffle,
                                                all_pairs_means, cluster_names)

    res = one_one_human_individual(interactions, cluster_pairs, clusters_counts, all_clusters, all_pairs_means)

    real_pvalues = res[0]
    real_percent = res[1]

    final_means = pd.DataFrame(columns=cluster_pairs)
    for key, value in all_pairs_means.items():
        for cluster in range(0, len(all_clusters)):
            for cluster2 in range(0, len(all_clusters)):
                cluster_interaction = "_".join([str(cluster_names[cluster]), str(cluster_names[cluster2])])
                target_cluster = all_pairs_means[key][cluster_interaction]
                real_p = real_pvalues.at[key, cluster_interaction]
                real_per = real_percent.at[key, cluster_interaction]

                sum_larger = 0
                for i in target_cluster:
                    sum_larger += i > real_p

                if (real_p == 0 or int(real_per) == 0):
                    p_val = 1
                else:
                    p_val = sum_larger / len(target_cluster)

                final_means.at[key, cluster_interaction] = p_val

    return (final_means, real_pvalues)


def filter_interactions_by_receptor_ligand(interactions: pd.DataFrame) -> pd.DataFrame:
    receptor_membrane = interactions[(interactions['receptor_1'] == True) &
                                     (interactions['secreted_highlight_2'] == False) &
                                     (interactions['source'] == 'curated')]

    membrane_receptor = interactions[(interactions['receptor_2'] == True) &
                                     (interactions['secreted_highlight_1'] == False) &
                                     (interactions['source'] == 'curated')]

    receptor_secreted = interactions[
        (interactions['receptor_1'] == True) & (interactions['other_1'] == False) &
        (interactions['secreted_highlight_2'] == True)]
    secreted_receptor = interactions[
        (interactions['receptor_2'] == True) & (interactions['other_2'] == False) &
        (interactions['secreted_highlight_1'] == True)]

    frames = [receptor_membrane, membrane_receptor, receptor_secreted, secreted_receptor]

    all_1_1_interactions = pd.concat(frames)
    all_1_1_interactions = all_1_1_interactions[all_1_1_interactions['score_2'] == 1]

    return all_1_1_interactions


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    genes = interactions['ensembl_1'].append(interactions['ensembl_2']).drop_duplicates()

    counts_filtered = counts.filter(genes, axis=0)

    return counts_filtered


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    ensembl_counts = counts.index
    interactions_filtered = interactions[interactions.apply(
        lambda row: row['ensembl_1'] in ensembl_counts and row['ensembl_2'] in ensembl_counts, axis=1
    )]
    return interactions_filtered


def filter_counts_by_genes(interactions: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    all_genes = interactions['ensembl_1'].tolist()
    all_genes.extend(interactions['ensembl_2'].tolist())
    genes_unique = set(all_genes)

    counts_filtered = counts.loc[counts.index.isin(genes_unique)]

    return counts_filtered


def cells_to_clusters(cluster_names: list, meta: pd.DataFrame, counts: pd.DataFrame) -> list:
    all_clusters = {}
    clusters_counts = {}
    cluster_means = []

    i = 0
    for x in cluster_names:
        all_clusters[i] = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % x)]).index
        clusters_counts[i] = counts.loc[:, all_clusters[i]]
        cluster_means.append(clusters_counts[i].apply(lambda counts: counts.mean(), axis=1))
        i = i + 1

    return [all_clusters, clusters_counts, cluster_means]


def filter_interactions_by_range(first_interaction: int, range: int, interactions: pd.DataFrame) -> pd.DataFrame:
    if (first_interaction + range) < len(interactions):
        interactions_filtered = interactions.iloc[first_interaction:first_interaction + range]
    else:
        interactions_filtered = interactions.iloc[first_interaction:len(interactions)]

    return interactions_filtered


def get_cluster_combinations(cluster_names: list) -> list:
    cluster_pairs = []
    for cluster in range(0, len(cluster_names)):
        for cluster2 in range(0, len(cluster_names)):
            cluster_pairs.append("_".join([str(cluster_names[cluster]), str(cluster_names[cluster2])]))

    return cluster_pairs


def filter_non_individual_interactions(interactions: pd.DataFrame) -> pd.DataFrame:
    interactions_filtered = interactions[
        interactions.apply(lambda interaction: interaction['ensembl_1'] != interaction['ensembl_2'], axis=1)]

    return interactions_filtered
