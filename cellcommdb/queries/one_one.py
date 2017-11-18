from datetime import datetime

import os
import pandas as pd
import numpy as np
from NaiveDE import lr_tests

from cellcommdb.api import create_app

from cellcommdb.models import *


def call(counts, meta):
    print('Query one-one started')

    interactions_df = _get_interactions()
    all_interactions = _filter_interactions_one_one(interactions_df, 1, 0.6)

    counts_filtered = _filter_counts_by_genes(counts, all_interactions)

    # cluster_names = ['Trophoblasts', 'Stromal_5', 'Stromal_13', 'Endothelial', 'M0', 'M2', 'M4', 'NK_6', 'NK_10', 'Cycling_NK', 'CD8', 'CD4', 'Tregs']
    cluster_names = meta['cell_type'].unique()
    start_time = datetime.now()

    # TODO: Delete me
    all_clusters = {}
    clusters_counts = {}

    i = 0
    for cluster_name in cluster_names:
        all_clusters[i] = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % cluster_name)]).index
        clusters_counts[i] = counts_filtered.loc[:, all_clusters[i]]
        i = i + 1

    print('{}'.format(datetime.now() - start_time))

    # TODO: End Delete me

    clusters = {}
    for cluster_name in cluster_names:
        cluster_cell_names = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % cluster_name)]).index
        clusters[cluster_name] = counts_filtered.loc[:, cluster_cell_names]

    #####  For each gene, count in how many clusters it is upregulated
    upregulated_result = _clusters_upregulated(clusters, counts_filtered)
    sum_upregulated = upregulated_result.sum(axis=1)
    sum_upregulated.to_csv('out/TEST_One_One_sum_upregulated.txt', sep="\t")

    permutations_pvalue = permutations_expressed(clusters_counts, 0, all_clusters, cluster_names, counts_filtered)
    one_one_human_interactions_permutations(all_interactions, 0, sum_upregulated, all_clusters, cluster_names,
                                            clusters_counts, permutations_pvalue)


    # permutations_pvalue = permutations_percent(clusters_counts, 0, 0.1, all_clusters, cluster_names, counts_filtered)
    # one_one_human_interactions_permutations(all_interactions, 0)


def _filter_counts_by_genes(counts, interactions):
    all_genes = interactions['ensembl_x'].tolist()
    all_genes.extend(interactions['ensembl_y'].tolist())
    genes_unique = set(all_genes)
    counts_filtered = counts.loc[counts.index.isin(genes_unique)]
    counts_filtered.to_csv('out/TEST_counts_filtered.csv')
    return counts_filtered


def _get_interactions():
    '''
    Gets the database interactions with gene/multidata info completed
    :rtype: pd.DataFrame()
    '''
    interactions_query = db.session.query(Interaction)
    interactions_df = pd.read_sql(interactions_query.statement, db.engine)

    multidata_query = db.session.query(Multidata, Gene.ensembl, Gene.gene_name).join(Protein).join(Gene)
    multidata_df = pd.read_sql(multidata_query.statement, db.engine)

    interactions_df.rename(index=str, columns={'id': 'interaction_id'}, inplace=True)
    interactions_df = pd.merge(interactions_df, multidata_df, left_on=['multidata_1_id'], right_on=['id'])
    interactions_df = pd.merge(interactions_df, multidata_df, left_on=['multidata_2_id'], right_on=['id'],
                               suffixes=['_x', '_y'])

    return interactions_df


def _filter_interactions_one_one(interactions_df, score_1, min_score_2):
    '''

    :type ineractions_df: pd.DataFrame()
    :rtype: pd.DataFrame()
    '''

    receptor_membrane = interactions_df[
        (interactions_df['receptor_x'] == True) &
        (interactions_df['transmembrane_y'] == True) &
        (interactions_df['secretion_y'] == False) &
        (interactions_df['transporter_y'] == False) &
        (interactions_df['cytoplasm_y'] == False) &
        (interactions_df['other_y'] == False)
        ]

    membrane_receptor = interactions_df[
        (interactions_df['receptor_y'] == True) &
        (interactions_df['transmembrane_x'] == True) &
        (interactions_df['secretion_x'] == False) &
        (interactions_df['transporter_x'] == False) &
        (interactions_df['cytoplasm_x'] == False) &
        (interactions_df['other_x'] == False)
        ]

    receptor_secreted = interactions_df[
        (interactions_df['receptor_x'] == True) &
        (interactions_df['secretion_y'] == True)
        ]

    secreted_receptor = interactions_df[
        (interactions_df['receptor_y'] == True) &
        (interactions_df['secretion_x'] == True)
        ]

    receptor_ligand_c = interactions_df[
        (interactions_df['receptor_x'] == True) &
        (interactions_df['ligand_y'] == True)
        ]

    ligand_receptor_c = interactions_df[
        (interactions_df['receptor_y'] == True) &
        (interactions_df['ligand_x'] == True)
        ]

    frames = [receptor_membrane, membrane_receptor, receptor_secreted, secreted_receptor, receptor_ligand_c,
              ligand_receptor_c]

    one_one_interactions = pd.concat(frames)

    one_one_interactions.drop_duplicates(inplace=True)

    one_one_interactions = one_one_interactions[
        (one_one_interactions['score_1'] == score_1) &
        (one_one_interactions['score_2'] > min_score_2)
        ]

    one_one_interactions.to_csv('out/TEST_one_one_interactions.csv', index=False)
    return one_one_interactions


#######    Permute each gene in each cluster, take randomly with replacement cells (as many as is the size of this cluster) from the specific cluster
#######    and in each permutation, save the mean. When you have 1000 means, you have a distribution of the means. Check if the total number of permutations
#######    lower than 0 divided by total number of permutations (1000) is lower than 0.05 (which is our threshold for significance)
#######    If yes, than the gene passed the test, put 1 in the output table; if not, put 0

def permutations_expressed(counts_matrix, threshold, all_clusters, new_clusters, counts_filtered):
    np.random.seed(123)
    df = pd.DataFrame()
    for cluster in range(0, len(all_clusters)):
        counts_cluster = counts_matrix[cluster]
        all_p = []
        for row, index in counts_cluster.iterrows():
            mean_g = []
            gene = row

            for x in range(0, 1000):
                a1 = np.random.choice(counts_cluster.loc[gene], len(counts_cluster.columns), replace=True)
                mean_g.append(np.mean(a1))
            mean_g = np.array(mean_g).tolist()
            p_val = float(sum(i <= threshold for i in mean_g)) / 1000
            if (p_val < 0.05):
                all_p.append(1)
            else:
                all_p.append(0)
        cluster_name = new_clusters[cluster]
        # df.assign(cluster_name=all_p)
        df[cluster_name] = pd.Series(all_p, index=counts_filtered.index)

    return df


#######    Permute each gene in each cluster, take randomly with replacement cells (as many as is the size of this cluster) from the specific cluster
#######    and in each permutation, save the % of cells which have expession of the specific gene > 0 (threshold). When you have 1000 percentages, you have a distribution of the percentages. Check if the total number of permutations
#######    lower than 10% (or input parameter percent) divided by total number of permutations (1000) is lower than 0.05 (which is our threshold for significance)
#######    If yes, than the gene passed the test, put the real % of cells expressing this gene in the output table; if not, put 0

def permutations_percent(counts_matrix, threshold, percent, all_clusters, new_clusters, counts_filtered):
    np.random.seed(123)
    df = pd.DataFrame()
    for cluster in range(0, len(all_clusters)):
        counts_cluster = counts_matrix[cluster]
        all_percent = []
        for row, index in counts_cluster.iterrows():
            mean_g = []
            gene = row

            for x in range(0, 1000):
                a1 = np.random.choice(counts_cluster.loc[gene], len(counts_cluster.columns), replace=True)
                mean_g.append(float(sum(i > threshold for i in a1)) / a1.size)
            mean_g = np.array(mean_g).tolist()
            p_val = float(sum(i <= percent for i in mean_g)) / 1000
            num_cells = len(counts_cluster.loc[gene][counts_cluster.loc[gene] > threshold])
            if (p_val < 0.05):
                all_percent.append(float(num_cells) / len(counts_cluster.columns))
            else:
                all_percent.append(0)

        cluster_name = new_clusters[cluster]
        # df.assign(cluster_name=all_p)
        df[cluster_name] = pd.Series(all_percent, index=counts_filtered.index)

    return df


def _clusters_upregulated(clusters, counts_filtered):
    '''
    Use NaiveDE (https://github.com/Teichlab/NaiveDE) for differential expression analysis - check for each gene, for
    each cluster, if the gene is upregulated in this cluster vs all other clusters. If the gene is significanlty
    upregulated in this cluster (q value < 0.1), then put 1 in output table, otherwise put 0

    :type clusters: pd.DataFrame()
    :type counts_filtered: pd.DataFrame()
    :rtype: pd.DataFrame()
    '''
    counts_filtered_log = np.log1p(counts_filtered)
    all_cells_names = counts_filtered_log.columns

    upregulated_clusters = pd.DataFrame(0, counts_filtered_log.index, clusters.keys())

    for cluster_name in clusters:
        counts_cluster = clusters[cluster_name]
        condition = pd.DataFrame(None, all_cells_names)
        condition['condition'] = 1

        for cell_name in counts_cluster.columns:
            condition.set_value(cell_name, 'condition', 0)

        expr = lr_tests(condition, counts_filtered_log, alt_model='~ condition', null_model='~ 1', rcond=-1)

        for index, qval in expr['qval'].iteritems():
            if qval < 0.1:
                upregulated_clusters.set_value(index, cluster_name, 1)

    upregulated_clusters.to_csv('out/TEST_upregulated.csv')

    return upregulated_clusters


######    Take all one-one interactions, for all clusters (cell types) iterate through each interaction
######    for each interaction, check both the partners (ligand and receptor) if they passed the permutation test
######    if they passed, for both genes take the sum of the upregulation table (count in how many clusters the gene is upregulated) Sum_Up_L and Sum_Up_R,
######    then sum both of the counts (for both partner genes of the interactions) and take the mean  - Mean_Sum - this will be used later to rank the interactions (low to high)
######    For genes for which the sum is 0, put artificial score - total number of clusters + 1  - so that they rank lower

def one_one_human_interactions_permutations(all_interactions, threshold, sum_upregulated, all_clusters, new_clusters,
                                            clusters_counts, permutations_pvalue):
    np.random.seed(123)

    # clean outfolder
    path = 'out/one-one'
    namefiles = os.listdir('%s' % path)
    for namefile in namefiles:
        if namefile.endswith('.txt'):
            os.remove('%s/%s' % (path, namefile))

    for cluster in range(0, len(all_clusters) - 1):
        columns = ['Unity_L', 'Gene_L', 'Receptor_L', 'Membrane_L', 'Secretion_L', 'Ligand_L', 'Adhesion_L',
                   'Unity_R', 'Gene_R', 'Receptor_R', 'Membrane_R', 'Secretion_R', 'Ligand_R', 'Adhesion_R',
                   'Total_Mean_L', 'Mean_L', 'Total_cells_L', 'Num_cells_L', 'Sum_Up_L', 'Total_Mean_R', 'Mean_R',
                   'Total_cells_R',
                   'Num_cells_R', 'Sum_Up_R', 'Mean_Sum']
        for cluster2 in range(0, len(all_clusters)):
            if cluster < cluster2:
                cluster_name = new_clusters[cluster]
                cluster2_name = new_clusters[cluster2]
                cluster_mean1 = []
                interaction_id1 = []
                cluster_mean2 = []
                interaction_id2 = []
                for row, index in all_interactions.iterrows():
                    receptor = index['ensembl_x']
                    ligand = index['ensembl_y']
                    gene_1 = index['gene_name_x']
                    gene_2 = index['gene_name_y']
                    if (receptor is not None) & (ligand is not None):
                        mm1 = clusters_counts[cluster]
                        mean_expr_r = 0
                        num_cells_r = 0
                        mm2 = clusters_counts[cluster2]
                        mean_expr_l = 0
                        num_cells_l = 0
                        mean_r = []
                        mean_l = []
                        if (receptor in mm1.index) & (ligand in mm2.index):
                            p_val_r = permutations_pvalue.loc[receptor, cluster_name]
                            p_val_l = permutations_pvalue.loc[ligand, cluster2_name]
                            mean_expr_r = mm1.loc[receptor].mean()
                            num_cells_r = len(mm1.loc[receptor][mm1.loc[receptor] > 0])
                            mean_expr_l = mm2.loc[ligand].mean()
                            num_cells_l = len(mm2.loc[ligand][mm2.loc[ligand] > 0])
                            total_cells_r = len(mm1.columns)
                            total_cells_l = len(mm2.columns)
                            if (p_val_l != 0) & (p_val_r != 0):
                                sum_r = sum_upregulated.loc[receptor]
                                sum_l = sum_upregulated.loc[ligand]
                                if (sum_r == 0):
                                    sum_r = float(len(all_clusters) + 1)
                                if (sum_l == 0):
                                    sum_l = float(len(all_clusters) + 1)

                                mean_sum = sum_r + sum_l
                                mean_sum = float(mean_sum) / 2

                                cluster_mean1.append(
                                    {'Unity_L': receptor, 'Gene_L': gene_1, 'Receptor_L': index['receptor_x'],
                                     'Membrane_L': index['transmembrane_x'],
                                     'Secretion_L': index['secretion_x'], 'Ligand_L': index['ligand_x'],
                                     'Adhesion_L': index['adhesion_x'],
                                     'Unity_R': ligand, 'Gene_R': gene_2, 'Receptor_R': index['receptor_y'],
                                     'Membrane_R': index['transmembrane_y'],
                                     'Secretion_R': index['secretion_y'], 'Ligand_R': index['ligand_y'],
                                     'Adhesion_R': index['adhesion_y'],
                                     'Total_Mean_L': mean_expr_r, 'Mean_L': np.mean(mean_r),
                                     'Total_cells_L': total_cells_r, 'Num_cells_L': num_cells_r, 'Sum_Up_L': sum_r,
                                     'Total_Mean_R': mean_expr_l, 'Mean_R': np.mean(mean_l),
                                     'Total_cells_R': total_cells_l, 'Num_cells_R': num_cells_l, 'Sum_Up_R': sum_l,
                                     'Mean_Sum': mean_sum})
                                interaction_id1.append(index['interaction_id'])

                    receptor2 = index['ensembl_y']
                    ligand2 = index['ensembl_x']
                    if (receptor2 is not None) & (ligand2 is not None):
                        mm1 = clusters_counts[cluster]
                        mean_expr_r = 0
                        num_cells_r = 0
                        mm2 = clusters_counts[cluster2]
                        mean_expr_l = 0
                        num_cells_l = 0
                        mean_r = []
                        mean_l = []
                        if (receptor2 in mm1.index) & (ligand2 in mm2.index):
                            p_val_r = permutations_pvalue.loc[receptor2, cluster_name]
                            p_val_l = permutations_pvalue.loc[ligand2, cluster2_name]
                            mean_expr_r = mm1.loc[receptor2].mean()
                            num_cells_r = len(mm1.loc[receptor2][mm1.loc[receptor2] > 0])
                            mean_expr_l = mm2.loc[ligand2].mean()
                            num_cells_l = len(mm2.loc[ligand2][mm2.loc[ligand2] > 0])
                            total_cells_r = len(mm1.columns)
                            total_cells_l = len(mm2.columns)

                            if (p_val_l != 0) & (p_val_r != 0):
                                sum_r = sum_upregulated.loc[receptor2]
                                sum_l = sum_upregulated.loc[ligand2]
                                if (sum_r == 0):
                                    sum_r = len(all_clusters) + 1
                                if (sum_l == 0):
                                    sum_l = len(all_clusters) + 1
                                mean_sum = sum_r + sum_l
                                mean_sum = float(mean_sum) / 2
                                cluster_mean2.append(
                                    {'Unity_L': receptor2, 'Gene_L': gene_2, 'Receptor_L': index['receptor_y'],
                                     'Membrane_L': index['transmembrane_y'],
                                     'Secretion_L': index['secretion_y'], 'Ligand_L': index['ligand_y'],
                                     'Adhesion_L': index['adhesion_y'],
                                     'Unity_R': ligand2, 'Gene_R': gene_1, 'Receptor_R': index['receptor_x'],
                                     'Membrane_R': index['transmembrane_x'],
                                     'Secretion_R': index['secretion_x'], 'Ligand_R': index['ligand_x'],
                                     'Adhesion_R': index['adhesion_x'],
                                     'Total_Mean_L': mean_expr_r, 'Mean_L': np.mean(mean_r),
                                     'Total_cells_L': total_cells_r, 'Num_cells_L': num_cells_r, 'Sum_Up_L': sum_r,
                                     'Total_Mean_R': mean_expr_l, 'Mean_R': np.mean(mean_l),
                                     'Total_cells_R': total_cells_l, 'Num_cells_R': num_cells_l, 'Sum_Up_R': sum_l,
                                     'Mean_Sum': mean_sum})
                                interaction_id2.append(index['interaction_id'])

                df1 = pd.DataFrame(cluster_mean1, index=interaction_id1, columns=columns)
                df2 = pd.DataFrame(cluster_mean2, index=interaction_id2, columns=columns)
                frames = [df1, df2]
                all_interactions_cluster = pd.concat(frames)
                all_interactions_cluster['Mean_Sum'].apply(pd.to_numeric)
                # all_interactions_cluster.sort_values('Mean_Sum', ascending=True)
                path_out = 'out/one-one/Cluster_%s_Cluster_%s_min%d.txt' % (
                    cluster_name, cluster2_name, threshold)
                all_interactions_cluster.to_csv(path_out, sep="\t")
