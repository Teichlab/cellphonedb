import datetime

import pandas as pd
from unittest import TestCase

import collections
import numpy as np

from methods.one_one_human_interactions_permutations import one_one_human_interactions_permutations, \
    one_one_human_individual
import methods_refactor
from utils import dataframe_functions


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    ensembl_counts = counts.index
    interactions_filtered = interactions[interactions.apply(
        lambda row: row['ensembl_x'] in ensembl_counts and row['ensembl_y'] in ensembl_counts, axis=1
    )]
    return interactions_filtered


def filter_counts_by_genes(interactions: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    all_genes = interactions['ensembl_x'].tolist()
    all_genes.extend(interactions['ensembl_y'].tolist())
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
        interactions.apply(lambda interaction: interaction['ensembl_x'] != interaction['ensembl_y'], axis=1)]

    return interactions_filtered


class TestOneOneHumanInteractionsPermutations(TestCase):
    np.random.seed(0)
    CPD_TEST = True
    iterations = 10
    how_many_interactions = 10

    all_interactions = pd.read_table('{}/one_one_interactions_filtered.txt'.format(methods_refactor.methods_input_data),
                                     index_col=0)

    interactions = filter_interactions_by_range(1, how_many_interactions, all_interactions)
    print('INTERACTIONS ORIGINAL: {}'.format(len(interactions)))

    if CPD_TEST:
        counts = pd.read_table('{}/test_counts.txt'.format(methods_refactor.methods_example_data), index_col=0)
        meta = pd.read_table('{}/test_meta.txt'.format(methods_refactor.methods_example_data), index_col=0)
        data_font = 'test'
    else:
        counts = pd.read_table('{}/counts.txt'.format(methods_refactor.methods_input_data), index_col=0)
        meta = pd.read_table('{}/metadata.txt'.format(methods_refactor.methods_input_data), index_col=0)
        data_font = 'original'

    print('[RUNNING][DATA:{}][ITERATIONS:{}][INTERACTIONS:{}]'.format(data_font, iterations, how_many_interactions))
    print('COUNTS ORIGINAL: {}'.format(len(counts)))
    counts_filtered = filter_counts_by_genes(interactions, counts)
    print('COUNTS TRIMED: {}'.format(len(counts_filtered)))
    interactions = filter_interactions_by_counts(interactions, counts)
    interactions = filter_non_individual_interactions(interactions)
    print('INTERACTIONS FILTERED: {}'.format(len(interactions)))

    cluster_names = meta.cell_type.unique()

    clusters_data = cells_to_clusters(cluster_names, meta, counts_filtered)

    all_clusters = clusters_data[0]
    clusters_counts = clusters_data[1]
    clusters_means = clusters_data[2]

    cluster_pairs = get_cluster_combinations(cluster_names)

    cells_values = meta['cell_type']
    cells_keys = meta.index
    cells_clusters = dict(zip(cells_keys, cells_values))

    all_pairs_means = collections.defaultdict(dict)
    #####   here we will save all the means from the 1000 shufflings, and we will use these 1000 values
    # per each interaction pair for each cluster-cluster analysis to calculate the p-value of the interaction pair for this cluster-cluster

    ######   Shuffling the cluster annotation of all cells - column names and creating the shuffled count tables for each cluster

    ### TIMES
    start_time = datetime.datetime.now()
    partials = []
    one_one_partials = []
    cell_to_clusters_partials = []
    print('[START] Shuffling the cluster annotation of all cells'.format(start_time))
    #####
    for count_r in range(1, iterations + 1):
        start_partial = datetime.datetime.now()

        clusters_values = sorted(cells_clusters.values())
        np.random.shuffle(clusters_values)

        new_meta = pd.DataFrame(
            {'Cell': sorted(cells_clusters.keys()),
             'cell_type': clusters_values
             })

        new_meta.set_index('Cell', inplace=True)
        cell_to_clusters_start_time = datetime.datetime.now()

        clusters_data_shuffle = cells_to_clusters(cluster_names, new_meta, counts_filtered)
        all_clusters_shuffle = clusters_data_shuffle[0]
        clusters_counts_shuffle = clusters_data_shuffle[1]
        clusters_means_shuffle = clusters_data_shuffle[2]

        ######    run the function to calculate mean of (receptor,ligand) for each of the 1000 shufflings
        interaction_permutations_start_time = datetime.datetime.now()

        cell_to_clusters_partials.append(
            (interaction_permutations_start_time - cell_to_clusters_start_time).microseconds)

        one_one_human_interactions_permutations(interactions, clusters_counts_shuffle, all_clusters_shuffle,
                                                clusters_means_shuffle, all_pairs_means, cluster_names)

        end_partial = datetime.datetime.now()
        one_one_partials.append((end_partial - interaction_permutations_start_time).microseconds)
        partial = end_partial - start_partial
        partials.append(partial.microseconds)

    end_time = datetime.datetime.now()

    # print(json.dumps(all_pairs_means))

    print('[END][TOTAL TIME] {}'.format(end_time - start_time))
    print('[AVG ITERATION TIME] {}'.format(sum(partials) / len(partials)))
    print('[MAX ITERATION TIME] {}'.format(max(partials)))
    print('[MIN ITERATION TIME] {}'.format(min(partials)))

    print('[AVG CELL_TO_CLUSTER TIME] {}'.format(sum(cell_to_clusters_partials) / len(cell_to_clusters_partials)))
    print('[MAX CELL_TO_CLUSTER TIME] {}'.format(max(cell_to_clusters_partials)))
    print('[MIN CELL_TO_CLUSTER TIME] {}'.format(min(cell_to_clusters_partials)))

    print('[AVG ONE_ONE TIME] {}'.format(sum(one_one_partials) / len(one_one_partials)))
    print('[MAX ONE_ONE TIME] {}'.format(max(one_one_partials)))
    print('[MIN ONE_ONE TIME] {}'.format(min(one_one_partials)))

    ############## END FIRST PART

    ######    run the function to calculate mean of (receptor,ligand) for the real unshuffled count matrix to calculate the real observed mean and
    # the % of cells expressing the ligand and the receptor in the specific clusters
    res = one_one_human_individual(interactions, cluster_pairs, clusters_counts, all_clusters, all_pairs_means)

    real_pvalues = res[0]
    real_percent = res[1]

    ######   calculate p-values for each interaction pair, for all cluster-cluster comparisons and save them in final_means

    final_means = pd.DataFrame(columns=cluster_pairs)
    for key, value in all_pairs_means.items():
        for cluster in range(0, len(all_clusters)):
            for cluster2 in range(0, len(all_clusters)):
                # if cluster <= cluster2:
                cluster_interaction = "_".join([str(cluster_names[cluster]), str(cluster_names[cluster2])])
                target_cluster = all_pairs_means[key][cluster_interaction]
                real_p = real_pvalues.at[key, cluster_interaction]
                real_per = real_percent.at[key, cluster_interaction]

                sum_larger = 0
                for i in target_cluster:
                    sum_larger += i > real_p

                # sum_larger = sum(i > asd for i in target_cluster)

                ####  check the % of cells expressing the receptor and ligand of the specific interaction, if the value is 0,
                # it means one or both of receptor/ligand were expressed in less than 20% of cells, so the p-value is not significant - put 1
                # (the lowest the p-value, the better the significance)
                if (real_p == 0 or int(real_per) == 0):
                    p_val = 1
                else:
                    p_val = sum_larger / len(target_cluster)

                final_means.at[key, cluster_interaction] = p_val

    file1 = '{}/test_r_m_pvalues_data-{}_it-{}_in-{}.txt'.format(methods_refactor.methods_output_data, data_font,
                                                                 iterations,
                                                                 how_many_interactions)
    final_means.sort_index().to_csv(file1, sep="\t")
    file2 = '{}/test_r_m_means_data-{}_it-{}_in-{}.txt'.format(methods_refactor.methods_output_data, data_font,
                                                               iterations, how_many_interactions)
    real_pvalues.to_csv(file2, sep="\t")

    original_means = pd.read_table(
        '{}/r_m_pvalues_data-{}_it-{}_in-{}.txt'.format(methods_refactor.methods_data_test_dir, data_font, iterations,
                                                        how_many_interactions),
        index_col=0)
    assert (dataframe_functions.dataframes_has_same_data(final_means.astype('float', copy=True),
                                                         original_means.astype('float', copy=True)))

    original_pvalues = pd.read_table(
        '{}/r_m_means_data-{}_it-{}_in-{}.txt'.format(methods_refactor.methods_data_test_dir, data_font, iterations,
                                                      how_many_interactions), index_col=0)
    assert (dataframe_functions.dataframes_has_same_data(real_pvalues.astype('float', copy=True),
                                                         original_pvalues.astype('float', copy=True),
                                                         round_decimals=True))
