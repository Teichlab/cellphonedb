
#!/usr/bin/env python
import os
import pandas as pd
import numpy as np
import math
import itertools
import collections
import scipy.stats
from numpy import *
import sys



num_interactions = sys.argv[1]
num_interactions = int(num_interactions)
how_many = sys.argv[2]
how_many = int(how_many)

def one_one_human_interactions_permutations(all_interactions, cluster_pairs, clusters_counts_shuffle, count_r):
    np.random.seed(123)

    interactions = pd.DataFrame(columns=cluster_pairs)
    all_means = pd.DataFrame(columns=cluster_pairs)
    df_percent = pd.DataFrame(columns=cluster_pairs)

    # print(len(cluster_pairs))
    for row, index in all_interactions.iterrows():
        if (index['ensembl_x'] != index['ensembl_y']) & (index['ensembl_x'] in counts_filtered.index) & (
            index['ensembl_y'] in counts_filtered.index):
            all_scores_1 = []
            all_means_1 = []
            all_percent = []

            for cluster in range(0, len(all_clusters)):
                for cluster2 in range(0, len(all_clusters)):

                    receptor = index['ensembl_x']
                    ligand = index['ensembl_y']

                    gene_1 = index['gene_name_x']
                    gene_2 = index['gene_name_y']

                    mm1 = clusters_counts_shuffle[cluster]
                    mm2 = clusters_counts_shuffle[cluster2]
                    mean_expr_r = mm1.loc[receptor].mean()
                    num_cells_r = len(mm1.loc[receptor][mm1.loc[receptor] > 0])
                    mean_expr_l = mm2.loc[ligand].mean()
                    num_cells_l = len(mm2.loc[ligand][mm2.loc[ligand] > 0])
                    total_cells_r = len(mm1.columns)
                    total_cells_l = len(mm2.columns)

                    if (count_r == 0):
                        if (float(num_cells_l) / total_cells_l < 0.2) | (float(num_cells_r) / total_cells_r < 0.2):
                            all_percent.append(0)
                        else:
                            all_percent.append(1)

                    if(mean_expr_l==0 or mean_expr_r==0):
                        total_mean=0
                    else:
                        total_mean = (mean_expr_r + mean_expr_l)/2

                    if (count_r != 0):
                        if ("_".join([str(gene_1), str(gene_2)]) in all_pairs_means.keys()):
                            if ("_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])]) in all_pairs_means[
                                "_".join([str(gene_1), str(gene_2)])].keys()):
                                all_pairs_means["_".join([str(gene_1), str(gene_2)])][
                                    "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])].append(
                                    total_mean)
                            else:
                                all_pairs_means["_".join([str(gene_1), str(gene_2)])][
                                    "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])] = [total_mean]
                        else:
                            all_pairs_means["_".join([str(gene_1), str(gene_2)])][
                                "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])] = [total_mean]

                    all_means_1.append(total_mean)

            if (count_r == 0):
                df_percent.loc["_".join([str(gene_1), str(gene_2)])] = all_percent
                all_means.loc["_".join([str(gene_1), str(gene_2)])] = all_means_1



    return [all_means, interactions, df_percent]



all_interactions = pd.read_table('one_one_interactions.txt', index_col=0)


if (num_interactions+how_many)<len(all_interactions):
    all_interactions = all_interactions.iloc[num_interactions:num_interactions+how_many]
else:
    all_interactions = all_interactions.iloc[num_interactions:len(all_interactions)]




counts = pd.read_table('counts.txt', index_col=0)
meta = pd.read_table('metadata.txt', index_col=0)

all_genes = all_interactions['ensembl_x'].tolist()
all_genes.extend(all_interactions['ensembl_y'].tolist())
genes_unique = set(all_genes)


counts_filtered = counts.loc[counts.index.isin(genes_unique)]


all_clusters = {}
clusters_counts = {}

new_clusters = meta.cell_type.unique()


i = 0
for x in new_clusters:
    all_clusters[i] = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % x)]).index
    clusters_counts[i] = counts_filtered.loc[:,all_clusters[i]]
    i = i + 1



cluster_pairs = []
for cluster in range(0, len(all_clusters)):
    for cluster2 in range(0, len(all_clusters)):
        #if cluster <= cluster2:
        cluster_pairs.append("_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])]))


cells_values = meta['cell_type']
cells_keys = meta.index
cells_clusters = dict(zip(cells_keys, cells_values))
print('................')



#all_pairs_means = defaultdict(defaultdict(list).copy)
all_pairs_means = collections.defaultdict(dict)

for count_r in range(1, 1001):
    clusters_values = list(cells_clusters.values())
    random.shuffle(clusters_values)

    new_meta = pd.DataFrame(
        {'Cell': list(cells_clusters.keys()),
         'cell_type': clusters_values
         })

    new_meta.set_index('Cell', inplace=True)
    all_clusters_shuffle = {}
    clusters_counts_shuffle = {}

    i = 0
    for x in new_clusters:
        all_clusters_shuffle[i] = pd.DataFrame(new_meta.loc[(new_meta['cell_type'] == '%s' % x)]).index
        clusters_counts_shuffle[i] = counts_filtered.loc[:, all_clusters_shuffle[i]]
        i = i + 1

    one_one_human_interactions_permutations(all_interactions,cluster_pairs,clusters_counts_shuffle,count_r)



res = one_one_human_interactions_permutations(all_interactions, cluster_pairs, clusters_counts, 0)
real_pvalues = res[0]
real_percent = res[1]


final_means = pd.DataFrame(columns=cluster_pairs)
for key,value in all_pairs_means.items():
    for cluster in range(0, len(all_clusters)):
        for cluster2 in range(0, len(all_clusters)):
            #if cluster <= cluster2:
            target_cluster = all_pairs_means[key]["_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])]
            real_p = real_pvalues.at[key,"_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])]
            real_per = real_percent.at[key, "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])]

            sum_larger = sum(i > real_p for i in target_cluster)

            if (real_p==0 or int(real_per)==0):
                p_val = 1
            else:
                p_val = sum_larger/len(target_cluster)


            final_means.at[key,"_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])] = p_val




file1 = 'r_m_pvalues_%d.txt' % (num_interactions)
final_means.to_csv(file1, sep="\t")
file2 = 'r_m_means_%d.txt' % (num_interactions)
real_pvalues.to_csv(file2, sep="\t")



