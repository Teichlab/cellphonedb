import pandas as pd


def one_one_human_individual(all_interactions, cluster_pairs, clusters_counts_shuffle, all_clusters, all_pairs_means):
    all_means = pd.DataFrame(columns=cluster_pairs)
    df_percent = pd.DataFrame(columns=cluster_pairs)

    for index, row in all_interactions.iterrows():
        all_means_1 = []
        all_percent = []
        receptor = row['ensembl_1']
        ligand = row['ensembl_2']

        gene_1 = row['gene_name_1']
        gene_2 = row['gene_name_2']

        for cluster in range(0, len(all_clusters)):
            for cluster2 in range(0, len(all_clusters)):

                mm1 = clusters_counts_shuffle[cluster]
                mm2 = clusters_counts_shuffle[cluster2]
                num_cells_r = len(mm1.loc[receptor][mm1.loc[receptor] > 0])
                num_cells_l = len(mm2.loc[ligand][mm2.loc[ligand] > 0])
                total_cells_r = len(mm1.columns)
                total_cells_l = len(mm2.columns)
                mean_expr_r = mm1.loc[receptor].mean()
                mean_expr_l = mm2.loc[ligand].mean()

                if (float(num_cells_l) / total_cells_l < 0.2) | (float(num_cells_r) / total_cells_r < 0.2):
                    all_percent.append(0)
                else:
                    all_percent.append(1)

                if (mean_expr_l == 0 or mean_expr_r == 0):
                    total_mean = 0
                else:
                    total_mean = (mean_expr_r + mean_expr_l) / 2

                all_means_1.append(total_mean)

        gene_interaction = "_".join([str(gene_1), str(gene_2)])
        df_percent.loc[gene_interaction] = all_percent
        all_means.loc[gene_interaction] = all_means_1

    return [all_means, df_percent]


def one_one_human_interactions_permutations(all_interactions, all_clusters, clusters_means, all_pairs_means,
                                            cluster_names):
    for index, row in all_interactions.iterrows():
        all_means_1 = []
        receptor = row['ensembl_1']
        ligand = row['ensembl_2']

        gene_1 = row['gene_name_1']
        gene_2 = row['gene_name_2']

        for cluster in range(0, len(all_clusters)):
            mean_expr_r = clusters_means[cluster][receptor]
            for cluster2 in range(0, len(all_clusters)):
                mean_expr_l = clusters_means[cluster2][ligand]

                gene_interaction = "_".join([str(gene_1), str(gene_2)])
                mean_expression_receptor_ligand(all_means_1, all_pairs_means, cluster, cluster2, mean_expr_l,
                                                mean_expr_r, cluster_names, gene_interaction)

    return all_pairs_means


def mean_expression_receptor_ligand(all_means_1, all_pairs_means, cluster, cluster2, mean_expr_l, mean_expr_r,
                                    cluster_names, gene_interaction):
    if (mean_expr_l == 0 or mean_expr_r == 0):
        total_mean = 0
    else:
        total_mean = (mean_expr_r + mean_expr_l) / 2

    cluster_interaction = "_".join([str(cluster_names[cluster]), str(cluster_names[cluster2])])

    if (gene_interaction in all_pairs_means.keys()):
        if (cluster_interaction in all_pairs_means[gene_interaction].keys()):
            all_pairs_means[gene_interaction][cluster_interaction].append(total_mean)
        else:
            all_pairs_means[gene_interaction][cluster_interaction] = [total_mean]
    else:
        all_pairs_means[gene_interaction][cluster_interaction] = [total_mean]

    all_means_1.append(total_mean)
