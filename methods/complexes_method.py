import os
import pandas as pd
import numpy as np
import math
import itertools
import collections
import scipy.stats
from numpy import *
import sys


current_dir = os.path.dirname(os.path.realpath(__file__))

np.random.seed(123)  #####   setting the random seed so that we get always same random shuffles

num_interactions = sys.argv[1]
num_interactions = int(num_interactions)
how_many = sys.argv[2]
how_many = int(how_many)


def get_proteins_in_complex_composition(complex):


    genes_query_df = pd.read_table('cellphonedb/genes.txt', index_col=0)


    complex_composition = pd.read_table('cellphonedb/complex_composition.txt', index_col=0)
    complex_composition_df = complex_composition.loc[complex_composition['complex_multidata_id'] == complex]

    proteins_query_df = pd.read_table('cellphonedb/proteins.txt', index_col=0)

    complex_proteins = pd.merge(complex_composition_df, proteins_query_df, left_on='protein_multidata_id',
                                right_on='protein_multidata_id')


    complex_proteins_genes = pd.merge(complex_proteins, genes_query_df, left_on='id_protein',
                                      right_on='protein_id')


    return complex_proteins_genes





def get_gene_for_multidata(multidata_id):
    genes_query_df = pd.read_table('cellphonedb/genes.txt', index_col=0)
    multidata_query_df = pd.read_table('cellphonedb/multidata.txt', index_col=0)
    proteins_query_df = pd.read_table('cellphonedb/proteins.txt', index_col=0)

    multidata_proteins = pd.merge(multidata_query_df, proteins_query_df, left_on='id_multidata',
                                right_on='protein_multidata_id')

    gene_protein_query = pd.merge(genes_query_df, multidata_proteins, left_on='protein_id',
                                      right_on='protein_multidata_id')

    gene_protein_df = gene_protein_query.loc[gene_protein_query['protein_multidata_id'] == multidata_id]
    gene_protein_df = gene_protein_df.ix[:, ['ensembl', 'gene_name']]


    return gene_protein_df




######  function where we input the real unshuffled count table to get the real means of expression of (receptor, ligand),
# and we find and save in lists all genes - members of the complexes in all_interactions that have minimum expression in cluster 1 (genes 1)
# and cluster 2 (genes 2), and we save also the % of cells expressing those minimum genes in the clusters, so that
# if the genes are expressed in less than 20% of the cells in the cluster, save 0, otherwise save 1

def complexes_interactions(all_interactions, cluster_pairs, clusters_counts):

    all_means = pd.DataFrame(columns=cluster_pairs)
    df_percent = pd.DataFrame(columns=cluster_pairs)
    genes1 = []
    genes2 = []
    # print(len(cluster_pairs))
    for row1, index1 in all_interactions.iterrows():

        all_means_1 = []
        all_percent = []

        for cluster in range(0, len(all_clusters)):
            for cluster2 in range(0, len(all_clusters)):


                proteins = get_proteins_in_complex_composition(index1['complex_multidata_id'])
                mean_r = []
                mm = clusters_counts[cluster]
                for row, index in proteins.iterrows():
                    pr = index['ensembl']
                    total_cells_r = len(mm.columns)
                    mean_r.append(mm.loc[pr].mean())
                val, idx = min((val, idx) for (idx, val) in enumerate(mean_r))
                min_receptor = proteins.iloc[idx]['ensembl']
                gene_1 = index1['name_x']
                mean_expr_r = mm.loc[min_receptor].mean()
                num_cells_r = len(mm.loc[min_receptor][mm.loc[min_receptor] > 0])
                genes1.append(min_receptor)

                if (index1['Complex'] == True):
                    proteins_2 = get_proteins_in_complex_composition(index1['multidata_2_id'])
                    genes_2 = []
                    mean_l = []
                    mm2 = clusters_counts[cluster2]
                    for row, index in proteins_2.iterrows():
                        pr = index['ensembl']
                        genes_2.append(index['gene_name'])
                        mean_l.append(mm2.loc[pr].mean())

                    val, idx = min((val, idx) for (idx, val) in enumerate(mean_l))
                    min_ligand = proteins_2.iloc[idx]['ensembl']
                    gene_2 = index1['name_y']
                    mean_expr_l = mm2.loc[min_ligand].mean()
                    total_cells_l = len(mm2.columns)
                    num_cells_l = len(mm2.loc[min_ligand][mm2.loc[min_ligand] > 0])
                    genes2.append(min_ligand)


                else:
                    genes_multidata = get_gene_for_multidata(index1['multidata_2_id'])
                    ligand = genes_multidata.iloc[0]['ensembl']
                    gene_2 = genes_multidata.iloc[0]['gene_name']
                    mm2 = clusters_counts[cluster2]
                    total_cells_l = len(mm2.columns)
                    mean_expr_l = mm2.loc[ligand].mean()
                    num_cells_l = len(mm2.loc[ligand][mm2.loc[ligand] > 0])
                    genes2.append(ligand)




                if (float(num_cells_l) / total_cells_l < 0.2) | (float(num_cells_r) / total_cells_r < 0.2):
                    all_percent.append(0)
                else:
                    all_percent.append(1)


                if (mean_expr_l == 0 or mean_expr_r == 0):
                    total_mean = 0
                else:
                    total_mean = (mean_expr_r + mean_expr_l) / 2



                all_means_1.append(total_mean)




        df_percent.loc["_".join([str(gene_1), str(gene_2)])] = all_percent
        all_means.loc["_".join([str(gene_1), str(gene_2)])] = all_means_1

    return [all_means, df_percent, genes1, genes2]






######  Function to calculate the mean (receptor, ligand) of each cluster-cluster analysis for each interaction pair
######  all_interactions  - dataframe with all interaction pairs already queried from the database and filtered (containing the ensembl and gene names of the receptor and ligand)
######  cluster_pairs - list of cluster_cluster names  - will be used to put column names on the final table
######  clusters_counts_shuffle - shuffled count table, where the columns of the original count table (the cells) are shuffled so that the cells now belong to different clusters
######  count_r - if this value is 0, calculate the % of cells expressing the receptor and ligand and real mean of expression of (receptor,ligand), using the original count matrix, not the shuffle
######  genes1 - list of genes - members of the complexes that are min expressed in cluster 1
######  genes2 - list of genes - members of the complexes that are min expressed in cluster 2 (in the cases where )
######  the complexes_interactions_shuffle will be performed 1000 times, each time, we calculate the mean and we save these values in a dictionary (all_pairs_means)



def complexes_interactions_shuffle(all_interactions, cluster_pairs, clusters_counts_shuffle, genes1, genes2):

    num = 0
    for row1, index1 in all_interactions.iterrows():

        all_means_1 = []

        for cluster in range(0, len(all_clusters)):
            for cluster2 in range(0, len(all_clusters)):
                # if cluster <= cluster2:

                mm = clusters_counts_shuffle[cluster]
                min_receptor = genes1[num]
                gene_1 = index1['name_x']
                mean_expr_r = mm.loc[min_receptor].mean()

                if (index1['Complex'] == True):

                    mm2 = clusters_counts_shuffle[cluster2]
                    min_ligand = genes2[num]
                    gene_2 = index1['name_y']
                    mean_expr_l = mm2.loc[min_ligand].mean()


                else:
                    genes_multidata = get_gene_for_multidata(index1['multidata_2_id'])
                    ligand = genes2[num]
                    gene_2 = genes_multidata.iloc[0]['gene_name']
                    mm2 = clusters_counts_shuffle[cluster2]
                    mean_expr_l = mm2.loc[ligand].mean()


                if (mean_expr_l == 0 or mean_expr_r == 0):
                    total_mean = 0
                else:
                    total_mean = (mean_expr_r + mean_expr_l) / 2

                if (count_r != 0):
                    if ("_".join([str(gene_1), str(gene_2)]) in all_pairs_means.keys()):
                        if ("_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])]) in all_pairs_means[
                            "_".join([str(gene_1), str(gene_2)])].keys()):
                            all_pairs_means["_".join([str(gene_1), str(gene_2)])][
                                "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])].append(total_mean)
                        else:
                            all_pairs_means["_".join([str(gene_1), str(gene_2)])][
                                "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])] = [total_mean]
                    else:
                        all_pairs_means["_".join([str(gene_1), str(gene_2)])][
                            "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])] = [total_mean]

                all_means_1.append(total_mean)






######  all complex interactions already queried and filtered
all_complex_interactions_filtered = pd.read_table('complexes.txt', index_col=0)




counts = pd.read_table('counts.txt', index_col=0)
meta = pd.read_table('metadata.txt', index_col=0)


#####  filter count matrix so that only the genes that are in the complex interaction list are there
all_complex_genes = []
remove_rows = []
for row1, index1 in all_complex_interactions_filtered.iterrows():
    proteins = get_proteins_in_complex_composition(index1['complex_multidata_id'])
    for row, index in proteins.iterrows():
        pr = index['ensembl']
        all_complex_genes.append(pr)
        if (pr not in counts.index):
            remove_rows.append(row1)
    if (index1['Complex']==True):
        proteins_2 = get_proteins_in_complex_composition(index1['multidata_2_id'])
        for row, index in proteins_2.iterrows():
            pr = index['ensembl']
            all_complex_genes.append(pr)
            if (pr not in counts.index):
                remove_rows.append(row1)

    else:
        genes_multidata = get_gene_for_multidata(index1['multidata_2_id'])
        name_ens = genes_multidata.iloc[0]['ensembl']
        all_complex_genes.append(name_ens)
        if (name_ens not in counts.index):
            remove_rows.append(row1)


genes_unique = set(all_complex_genes)

counts_filtered = counts.loc[counts.index.isin(genes_unique)]



##### start the analysis from the specific pair and run it on "how_many" pairs

if (num_interactions+how_many)<len(all_complex_interactions_filtered):
    all_complex_interactions_filtered = all_complex_interactions_filtered.iloc[num_interactions:num_interactions+how_many]
else:
    all_complex_interactions_filtered = all_complex_interactions_filtered.iloc[num_interactions:len(all_complex_interactions_filtered)]


all_clusters = {}
clusters_counts = {}


######   get the cluster annotations - the meta data should have a column named "cell_type"
new_clusters = meta.cell_type.unique()


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



#####  run this funtion with the real unshuffled count data to get the real means, % of cells expressing the receptor and ligand
# in the specific clusters and to get the genes - members of the complexes with min expression in the specific cluster
# these genes will be used for the shuffling
res = complexes_interactions(all_complex_interactions_filtered, cluster_pairs, clusters_counts)
real_pvalues = res[0]
real_percent = res[1]
genes1 = res[2]
genes2 = res[3]



###### do the shuffling and create the shuffled count tables for each cluster

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

    ######   creating the shuffled count tables for each cluster

    i = 0
    for x in new_clusters:
        all_clusters_shuffle[i] = pd.DataFrame(new_meta.loc[(new_meta['cell_type'] == '%s' % x)]).index
        clusters_counts_shuffle[i] = counts_filtered.loc[:, all_clusters_shuffle[i]]
        i = i + 1

    ######    run the function to calculate mean of (receptor,ligand) for each of the 1000 shufflings
    complexes_interactions_shuffle(all_complex_interactions_filtered,cluster_pairs,clusters_counts_shuffle, genes1, genes2)



final_means = pd.DataFrame(columns=cluster_pairs) #####   here we will save all the means from the 1000 shufflings, and we will use these 1000 values
# per each interaction pair for each cluster-cluster analysis to calculate the p-value of the interaction pair for this cluster-cluster


######   calculate p-values for each interaction pair, for all cluster-cluster comparisons and save them in final_means

for key,value in all_pairs_means.items():
    for cluster in range(0, len(all_clusters)):
        for cluster2 in range(0, len(all_clusters)):
            #if cluster <= cluster2:
            target_cluster = all_pairs_means[key]["_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])]
            real_p = real_pvalues.at[key,"_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])]
            real_per = real_percent.at[key, "_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])]

            sum_larger = sum(i > real_p for i in target_cluster)

            ####  check the % of cells expressing the receptor and ligand of the specific interaction, if the value is 0,
            # it means one or both of receptor/ligand were expressed in less than 20% of cells, so the p-value is not significant - put 1
            # (the lowest the p-value, the better the significance)
            if (real_p==0 or int(real_per)==0):
                p_val = 1
            else:
                p_val = sum_larger/len(target_cluster)


            final_means.at[key,"_".join([str(new_clusters[cluster]), str(new_clusters[cluster2])])] = p_val




path_1 = 'complexes_pvalues_%d.txt' % (num_interactions)   ######   save pvalues for the specific interactions starting from num_interactions
final_means.to_csv(path_1, sep="\t")
path_2 = 'complexes_pvalues_%d.txt' % (num_interactions)   ######   save means for the specific interactions starting from num_interactions
real_pvalues.to_csv(path_2, sep="\t")


