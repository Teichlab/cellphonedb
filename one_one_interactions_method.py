
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


#######   Input arguments from command line

num_interactions = sys.argv[1]  ####   from which interactions pair to start
num_interactions = int(num_interactions)
how_many = sys.argv[2]     ##### on how many pairs should it run, starting from interaction pair on position "num_interactions"
how_many = int(how_many)


######  Function to calculate the mean (receptor, ligand) of each cluster-cluster analysis for each interaction pair
######  all_interactions  - dataframe with all interaction pairs already queried from the database and filtered (containing the ensembl and gene names of the receptor and ligand)
######  cluster_pairs - list of cluster_cluster names  - will be used to put column names on the final table
######  clusters_counts_shuffle - shuffled count table, where the columns of the original count table (the cells) are shuffled so that the cells now belong to different clusters
######  count_r - if this value is 0, calculate the % of cells expressing the receptor and ligand and real mean of expression of (receptor,ligand), using the original count matrix, not the shuffle
######  the one_one_human_interactions_permutations will be performed 1000 times, each time, we calculate the mean and we save these values in a dictionary (all_pairs_means)


def one_one_human_interactions_permutations(all_interactions, cluster_pairs, clusters_counts_shuffle, count_r):
    np.random.seed(123)

    all_means_1 = pd.DataFrame(columns=cluster_pairs)
    df_percent = pd.DataFrame(columns=cluster_pairs)

    # print(len(cluster_pairs))
    for row, index in all_interactions.iterrows():
        if (index['ensembl_x'] != index['ensembl_y']) & (index['ensembl_x'] in counts_filtered.index) & (
            index['ensembl_y'] in counts_filtered.index):
            all_means = []
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


                    ######   check if both receptor and ligand are expressed in min 20% of the cells in the specific clusters, if yes put 1, if no put 0
                    if (count_r == 0):
                        if (float(num_cells_l) / total_cells_l < 0.2) | (float(num_cells_r) / total_cells_r < 0.2):
                            all_percent.append(0)
                        else:
                            all_percent.append(1)


                    #######    Calculation of the mean of expression of (receptor,ligand)
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



    return [all_means, df_percent]



all_interactions = pd.read_table('one_one_interactions.txt', index_col=0)      ######   the dataframe of interaction pairs queried from the database and filtered



##### start the analysis from the specific pair and run it on "how_many" pairs

if (num_interactions+how_many)<len(all_interactions):
    all_interactions = all_interactions.iloc[num_interactions:num_interactions+how_many]
else:
    all_interactions = all_interactions.iloc[num_interactions:len(all_interactions)]




counts = pd.read_table('counts.txt', index_col=0)   ####   count table
meta = pd.read_table('metadata.txt', index_col=0)   ####   meta data - cluster annotation should be column named "cell_type"

all_genes = all_interactions['ensembl_x'].tolist()
all_genes.extend(all_interactions['ensembl_y'].tolist())
genes_unique = set(all_genes)


counts_filtered = counts.loc[counts.index.isin(genes_unique)]   ######   filter the count table so that it contains only genes (rows) that are in the interaction pairs list


all_clusters = {}
clusters_counts = {}

new_clusters = meta.cell_type.unique()      #####   save the names of all clusters



#######    make separate count dataframes for each cluster
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



all_pairs_means = collections.defaultdict(dict)   #####   here we will save all the means from the 1000 shufflings, and we will use these 1000 values
# per each interaction pair for each cluster-cluster analysis to calculate the p-value of the interaction pair for this cluster-cluster



######   Shuffling the cluster annotation of all cells - column names and creating the shuffled count tables for each cluster
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


    ######   creating the shuffled count tables for each cluster
    i = 0
    for x in new_clusters:
        all_clusters_shuffle[i] = pd.DataFrame(new_meta.loc[(new_meta['cell_type'] == '%s' % x)]).index
        clusters_counts_shuffle[i] = counts_filtered.loc[:, all_clusters_shuffle[i]]
        i = i + 1

    ######    run the function to calculate mean of (receptor,ligand) for each of the 1000 shufflings
    one_one_human_interactions_permutations(all_interactions,cluster_pairs,clusters_counts_shuffle,count_r)



######    run the function to calculate mean of (receptor,ligand) for the real unshuffled count matrix to calculate the real observed mean and
# the % of cells expressing the ligand and the receptor in the specific clusters
res = one_one_human_interactions_permutations(all_interactions, cluster_pairs, clusters_counts, 0)
real_pvalues = res[0]
real_percent = res[1]



######   calculate p-values for each interaction pair, for all cluster-cluster comparisons and save them in final_means

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




file1 = 'r_m_pvalues_%d.txt' % (num_interactions)     ######   save pvalues for the specific interactions starting from num_interactions
final_means.to_csv(file1, sep="\t")
file2 = 'r_m_means_%d.txt' % (num_interactions)       ######   save means for the specific interactions starting from num_interactions
real_pvalues.to_csv(file2, sep="\t")



