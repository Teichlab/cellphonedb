import os
import pandas as pd
import numpy as np


from cellcommdb.api import create_app, data_dir

current_dir = os.path.dirname(os.path.realpath(__file__))

from cellcommdb.models import *

app = create_app()


def call(counts, meta):
    all_complex_interactions = query_receptor_secreted_complex_interactions()
    all_complex_genes = []

    for row1, index1 in all_complex_interactions.iterrows():
        proteins = get_proteins_in_complex_composition(index1['complex_multidata_id'])
        for row, index in proteins.iterrows():
            pr = index['ensembl']
            all_complex_genes.append(pr)
        if (index1['Complex'] == True):
            proteins_2 = get_proteins_in_complex_composition(index1['multidata_2_id'])
            for row, index in proteins_2.iterrows():
                pr = index['ensembl']
                all_complex_genes.append(pr)
        else:
            genes_multidata = get_gene_for_multidata(index1['multidata_2_id'])
            name_ens = genes_multidata.iloc[0]['ensembl']
            all_complex_genes.append(name_ens)

    genes_unique = set(all_complex_genes)

    counts_filtered = counts.loc[counts.index.isin(genes_unique)]
    counts_filtered.to_csv('out/ss2_complex_filtered_counts.txt', sep="\t")

    all_clusters = {}
    clusters_counts = {}

    # new_clusters = meta.cell_type.unique()
    # print(new_clusters)
    new_clusters = ['Trophoblasts', 'Stromal', 'Endothelial', 'Epithelial', 'Muscle', 'Pericytes', 'M_2', 'M_7',
                    'M1_11', 'Cycling_M', 'NK_5', 'NK_8', 'Cycling_NK', 'CD8', 'CD4', 'Tregs', 'Cycling_T', 'ILC']

    i = 0
    for x in new_clusters:
        all_clusters[i] = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % x)]).index
        clusters_counts[i] = counts_filtered.loc[:, all_clusters[i]]
        i = i + 1

    ######     log-transform the count table for differential expression analysis
    counts_filtered_log = np.log1p(counts_filtered)


    permutations_pvalue = expression_percent(clusters_counts, 0, 0.1, all_clusters, new_clusters,
                                               counts_filtered)
    complex_interactions_permutations(all_complex_interactions, 0, all_clusters, new_clusters,
                                      clusters_counts, permutations_pvalue)


# permutations_pvalue = permutations_percent(clusters_counts, 0, 0.1)
# complex_interactions_permutations(all_complex_interactions, 0, sum_upregulated)


#####  Query all Receptor-Secreted interactions with a complex
def query_receptor_secreted_complex_interactions():
    with app.app_context():
        ######  Genes

        genes_query = db.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement, db.engine)

        ######  Proteins

        proteins_query = db.session.query(Protein)
        proteins_df = pd.read_sql(proteins_query.statement, db.engine)

        proteins_genes = pd.merge(proteins_df, genes_query_df, left_on='id',
                                  right_on='protein_id')
        proteins_genes.rename(index=str, columns={'id_x': 'protein_id'}, inplace=True)
        proteins_genes.rename(index=str, columns={'id_y': 'gene_id'}, inplace=True)
        proteins_genes.rename(index=str, columns={'gene_name_y': 'gene_name'}, inplace=True)
        proteins_genes.drop(['gene_name_x'], axis=1, inplace=True)

        ######  Interactions

        interactions_query = db.session.query(Interaction)
        all_interactions_df = pd.read_sql(interactions_query.statement, db.engine)

        ######  Multidata

        multidata_query = db.session.query(Multidata)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)
        complex_query = db.session.query(Complex)
        complex_df = pd.read_sql(complex_query.statement, db.engine)

        # complex_unity_df.to_csv('out/complex_multidata.csv', sep="\t")

        complex_interactions_1_df = pd.merge(complex_df, all_interactions_df, left_on='complex_multidata_id',
                                             right_on='multidata_1_id')
        complex_interactions_2_df = pd.merge(complex_df, all_interactions_df, left_on='complex_multidata_id',
                                             right_on='multidata_2_id')
        complex_interactions_1_df.rename(index=str, columns={'id_y': 'interaction_id'}, inplace=True)
        complex_interactions_2_df.rename(index=str, columns={'id_y': 'interaction_id'}, inplace=True)
        complex_interactions_1_df.rename(index=str, columns={'id_x': 'complex_id'}, inplace=True)
        complex_interactions_2_df.rename(index=str, columns={'id_x': 'complex_id'}, inplace=True)

        complex_interactions_1_multidata_df = pd.merge(complex_interactions_1_df, multidata_df,
                                                       left_on='complex_multidata_id', right_on='id')

        complex_composition_query = db.session.query(ComplexComposition)
        complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)

        interactions_1_multidata_df = pd.merge(complex_interactions_1_multidata_df, multidata_df,
                                               left_on='multidata_2_id', right_on='id')
        complexes = [False] * len(interactions_1_multidata_df.index)
        interactions_1_multidata_df['Complex'] = complexes
        interactions_1_multidata_df.loc[interactions_1_multidata_df['multidata_2_id'].isin(
            complex_composition_df['complex_multidata_id']), 'Complex'] = True
        all_complex_interactions = interactions_1_multidata_df

        all_complex_interactions.to_csv('out/complex_all.txt', sep="\t")

        receptor_secreted_c = all_complex_interactions[
            (all_complex_interactions['receptor_x'] == True) & (all_complex_interactions['secretion_y'] == True)
            & (all_complex_interactions['other_y'] == False)]
        secreted_receptor_c = all_complex_interactions[
            (all_complex_interactions['receptor_y'] == True) & (all_complex_interactions['secretion_x'] == True)
            & (all_complex_interactions['other_x'] == False)]

        # frames_c = [receptor_secreted_c, secreted_receptor_c, receptor_membrane_c, membrane_receptor_c, receptor_ligand_c, ligand_receptor_c, receptor_adhesion_c, adhesion_receptor_c]
        frames_c = [receptor_secreted_c, secreted_receptor_c]
        interactions_complex = pd.concat(frames_c)
        interactions_complex.drop(['id_x'], axis=1, inplace=True)
        interactions_complex.drop(['id_y'], axis=1, inplace=True)



        return interactions_complex


#####  Query all Receptor-Membrane interactions with a complex

def query_R_M_complex_interactions():
    with app.app_context():
        ######  Genes

        genes_query = db.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement, db.engine)

        ######  Proteins

        proteins_query = db.session.query(Protein)
        proteins_df = pd.read_sql(proteins_query.statement, db.engine)

        proteins_genes = pd.merge(proteins_df, genes_query_df, left_on='id',
                                  right_on='protein_id')
        proteins_genes.rename(index=str, columns={'id_x': 'protein_id'}, inplace=True)
        proteins_genes.rename(index=str, columns={'id_y': 'gene_id'}, inplace=True)
        proteins_genes.rename(index=str, columns={'gene_name_y': 'gene_name'}, inplace=True)
        proteins_genes.drop(['gene_name_x'], axis=1, inplace=True)

        ######  Interactions

        interactions_query = db.session.query(Interaction)
        all_interactions_df = pd.read_sql(interactions_query.statement, db.engine)

        ######  Multidata

        multidata_query = db.session.query(Multidata)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)
        complex_query = db.session.query(Complex)
        complex_df = pd.read_sql(complex_query.statement, db.engine)

        # complex_unity_df.to_csv('out/complex_multidata.csv', sep="\t")

        complex_interactions_1_df = pd.merge(complex_df, all_interactions_df, left_on='complex_multidata_id',
                                             right_on='multidata_1_id')
        complex_interactions_2_df = pd.merge(complex_df, all_interactions_df, left_on='complex_multidata_id',
                                             right_on='multidata_2_id')
        complex_interactions_1_df.rename(index=str, columns={'id_y': 'interaction_id'}, inplace=True)
        complex_interactions_2_df.rename(index=str, columns={'id_y': 'interaction_id'}, inplace=True)
        complex_interactions_1_df.rename(index=str, columns={'id_x': 'complex_id'}, inplace=True)
        complex_interactions_2_df.rename(index=str, columns={'id_x': 'complex_id'}, inplace=True)

        complex_interactions_1_multidata_df = pd.merge(complex_interactions_1_df, multidata_df,
                                                       left_on='complex_multidata_id', right_on='id')

        complex_composition_query = db.session.query(ComplexComposition)
        complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)

        interactions_1_multidata_df = pd.merge(complex_interactions_1_multidata_df, multidata_df,
                                               left_on='multidata_2_id', right_on='id')
        complexes = [False] * len(interactions_1_multidata_df.index)
        interactions_1_multidata_df['Complex'] = complexes
        interactions_1_multidata_df.loc[interactions_1_multidata_df['multidata_2_id'].isin(
            complex_composition_df['complex_multidata_id']), 'Complex'] = True
        all_complex_interactions = interactions_1_multidata_df

        receptor_membrane_c = all_complex_interactions[
            (all_complex_interactions['receptor_x'] == True) & (all_complex_interactions['transmembrane_y'] == True)
            & (all_complex_interactions['transporter_y'] == False) & (all_complex_interactions['secretion_y'] == False)
            & (all_complex_interactions['other_y'] == False) & (all_complex_interactions['cytoplasm_y'] == False) &
            (all_complex_interactions['extracellular_y'] == True)]

        membrane_receptor_c = all_complex_interactions[
            (all_complex_interactions['receptor_y'] == True) & (all_complex_interactions['transmembrane_x'] == True)
            & (all_complex_interactions['transporter_x'] == False) & (all_complex_interactions['secretion_x'] == False)
            & (all_complex_interactions['other_x'] == False) & (all_complex_interactions['cytoplasm_x'] == False) &
            (all_complex_interactions['extracellular_x'] == True)]

        # frames_c = [receptor_secreted_c, secreted_receptor_c, receptor_membrane_c, membrane_receptor_c, receptor_ligand_c, ligand_receptor_c, receptor_adhesion_c, adhesion_receptor_c]
        frames_c = [receptor_membrane_c, membrane_receptor_c]
        interactions_complex = pd.concat(frames_c)
        interactions_complex.drop(['id_x'], axis=1, inplace=True)
        interactions_complex.drop(['id_y'], axis=1, inplace=True)

        return interactions_complex


######    Query all genes for a specific complex

def get_proteins_in_complex_composition(complex):
    with app.app_context():
        ######  Genes

        genes_query = db.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement, db.engine)

        ######  Proteins - multidata

        multidata_query = db.session.query(Multidata)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)

        complex_composition_query = db.session.query(ComplexComposition).filter(
            ComplexComposition.complex_multidata_id == complex)
        complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)

        proteins_query = db.session.query(Protein)
        proteins_query_df = pd.read_sql(proteins_query.statement, db.engine)

        complex_proteins = pd.merge(complex_composition_df, proteins_query_df, left_on='protein_multidata_id',
                                    right_on='protein_multidata_id')
        complex_proteins.to_csv('out/test3.csv', index=False)

        complex_proteins.rename(index=str, columns={'id_y': 'protein_id'}, inplace=True)
        complex_proteins.rename(index=str, columns={'id_x': 'complex_composition_id'}, inplace=True)

        complex_proteins_genes = pd.merge(complex_proteins, genes_query_df, left_on='protein_id',
                                          right_on='protein_id')
        complex_proteins_genes.rename(index=str, columns={'id': 'gene_id'}, inplace=True)
        # complex_proteins_genes.rename(index=str, columns={'gene_name_y': 'gene_name'}, inplace=True)
        # complex_proteins_genes.drop(['gene_name_x'], axis=1, inplace=True)



        return complex_proteins_genes


def get_gene_for_multidata(multidata_id):
    with app.app_context():
        gene_protein_query = db.session.query(Gene.ensembl, Gene.gene_name).join(Protein).filter(
            Protein.protein_multidata_id == multidata_id)
        gene_protein_df = pd.read_sql(gene_protein_query.statement, db.engine)
        gene_protein_df.to_csv('out/test2.csv', index=multidata_id)
        # print(complex_proteins_genes.shape)

        return gene_protein_df



def expression_percent(counts_matrix, threshold, percent, all_clusters, new_clusters,
                                               counts_filtered):
    df = pd.DataFrame()
    for cluster in range(0, len(all_clusters)):
        counts_cluster = counts_matrix[cluster]
        all_percent = []
        for row, index in counts_cluster.iterrows():
            mean_g = []
            gene = row
            num_cells = len(counts_cluster.loc[gene][counts_cluster.loc[gene] > threshold])
            perc = float(num_cells) / len(counts_cluster.columns)
            if (perc > percent):
                all_percent.append(perc)
            else:
                all_percent.append(0)

        cluster_name = new_clusters[cluster]
        # df.assign(cluster_name=all_p)
        df[cluster_name] = pd.Series(all_percent, index=counts_filtered.index)

    return df


######    Take all interactions with complexes, for all clusters (cell types) iterate through each interaction
######    for each interaction, if the partner is a complex, take all genes part of the complex, check if all genes of the complex passed the permutation test
######    Check the other partner of the interaction that is not a complex - if the gene passed the permutation test
######    if they passed, for all genes of the complex take the sum of the upregulation table (count in how many clusters the gene is upregulated) and take the mean of this count -  Sum_Up_L or Sum_Up_R,
######    For the other interaction partner that is not a complex, take the sum from the upregulation table
######    then sum both of the counts (the mean value for the complex and count for the not-complex partner) and take the mean  - Mean_Sum - this will be used later to rank the interactions (low to high)
######    For genes for which the sum is 0, put artificial score - total number of clusters + 1  - so that they rank lower


def complex_interactions_permutations(all_complex_interactions, threshold, all_clusters, new_clusters,
                                      clusters_counts, permutations_pvalue):
    for cluster in range(0, len(all_clusters) - 1):
        columns = ['Unity_L', 'Name_L', 'Gene_L', 'Gene_L_ens', 'Receptor_L', 'Membrane_L', 'Secretion_L', 'Ligand_L',
                   'Adhesion_L', 'Unity_R', 'Name_R', 'Gene_R', 'Gene_R_ens', 'Receptor_R', 'Membrane_R', 'Secretion_R',
                   'Ligand_R',
                   'Adhesion_R', 'Total_Mean_L', 'Mean_L', 'Total_cells_L', 'Num_cells_L', 'Total_Mean_R',
                   'Mean_R', 'Total_cells_R',
                   'Num_cells_R']
        for cluster2 in range(0, len(all_clusters)):
            if cluster <= cluster2:
                cluster_name = new_clusters[cluster]
                cluster2_name = new_clusters[cluster2]
                cluster_mean1 = []
                interaction_id1 = []
                cluster_mean2 = []
                interaction_id2 = []
                # df = pd.DataFrame(data=np.zeros((0, len(columns))), columns=columns)
                for row1, index1 in all_complex_interactions.iterrows():
                    proteins = get_proteins_in_complex_composition(index1['complex_multidata_id'])
                    complexes_mean_1 = []
                    complexes_cells_1 = []
                    complexes_num_1 = []
                    genes_ens_1 = []
                    genes_1 = []
                    mean_r = []
                    percentage_permutation = []
                    for row, index in proteins.iterrows():
                        pr = index['ensembl']
                        if (pr is not None):
                            mm = clusters_counts[cluster]
                            total_cells_r = len(mm.columns)
                            if (pr in mm.index):
                                mean_expr = mm.loc[pr].mean()
                                num_cells = len(mm.loc[pr][mm.loc[pr] > 0])
                                complexes_mean_1.append(mean_expr)
                                if (mean_expr > 0):
                                    complexes_num_1.append('yes')
                                complexes_cells_1.append(num_cells)
                                genes_ens_1.append(pr)
                                genes_1.append(index['gene_name'])
                                mean_r.append((mm.loc[pr][mm.loc[pr] > 0]).mean())
                                percentage_permutation.append(permutations_pvalue.loc[pr, cluster_name])

                    if (index1['Complex'] == True):
                        proteins_2 = get_proteins_in_complex_composition(index1['multidata_2_id'])
                        complexes_mean_2 = []
                        complexes_cells_2 = []
                        complexes_num_2 = []
                        genes_ens_2 = []
                        genes_2 = []
                        mean_l = []
                        for row, index in proteins_2.iterrows():
                            pr = index['ensembl']
                            if (pr is not None):
                                mm2 = clusters_counts[cluster2]
                                total_cells_l = len(mm2.columns)
                                if (pr in mm2.index):
                                    mean_expr_l = mm2.loc[pr].mean()
                                    num_cells_l = len(mm2.loc[pr][mm2.loc[pr] > 0])
                                    complexes_mean_2.append(mean_expr)
                                    if (mean_expr > 0):
                                        complexes_num_2.append('yes')
                                    complexes_cells_2.append(num_cells_l)
                                    genes_ens_2.append(pr)
                                    genes_2.append(index['gene_name'])
                                    mean_l.append((mm2.loc[pr][mm2.loc[pr] > 0]).mean())
                                    percentage_permutation.append(permutations_pvalue.loc[pr, cluster2_name])

                        if (all(percentage_permutation) != 0):
                            cluster_mean1.append(
                                {'Unity_L': index1['multidata_1_id'], 'Name_L': name_l, 'Gene_L': list(genes_1),
                                 'Gene_L_ens': list(genes_ens_1), 'Receptor_L': index1['receptor_x'],
                                 'Membrane_L': index1['transmembrane_x'], 'Secretion_L': index1['secretion_x'],
                                 'Ligand_L': index1['ligand_x'], 'Adhesion_L': index1['adhesion_x'],
                                 'Unity_R': index1['multidata_2_id'], 'Name_R': name_r, 'Gene_R': list(genes_2),
                                 'Gene_R_ens': list(genes_ens_2), 'Receptor_R': index1['receptor_y'],
                                 'Membrane_R': index1['transmembrane_y'], 'Secretion_R': index1['secretion_y'],
                                 'Ligand_R': index1['ligand_y'], 'Adhesion_R': index1['adhesion_y'],
                                 'Total_Mean_L': list(complexes_mean_1), 'Mean_L': list(mean_r),
                                 'Total_cells_L': total_cells_r, 'Num_cells_L': list(complexes_cells_1),
                                 'Total_Mean_R': list(complexes_mean_2), 'Mean_R': list(mean_l),
                                 'Total_cells_R': total_cells_l, 'Num_cells_R': list(complexes_cells_2)})
                            interaction_id1.append(index1['interaction_id'])
                    else:
                        genes_multidata = get_gene_for_multidata(index1['multidata_2_id'])
                        ligand = genes_multidata.iloc[0]['ensembl']
                        gene2 = genes_multidata.iloc[0]['gene_name']
                        name_l = index1['name_x']
                        name_r = index1['name_y']
                        # if (len(complexes_num_1) == len(proteins)) & (complexes_mean_1.mean()>5) & (ligand is not None):
                        if (ligand is not None):
                            mm2 = clusters_counts[cluster2]
                            mean_expr_l = 0
                            num_cells_l = 0
                            total_cells_l = len(mm2.columns)
                            if (ligand in mm2.index):
                                mean_expr_l = mm2.loc[ligand].mean()
                                num_cells_l = len(mm2.loc[ligand][mm2.loc[ligand] > 0])
                                mean_l = (mm2.loc[ligand][mm2.loc[ligand] > 0]).mean()
                                percentage_permutation.append(permutations_pvalue.loc[ligand, cluster2_name])

                        if (all(percentage_permutation) != 0):
                            cluster_mean1.append(
                                {'Unity_L': index1['multidata_1_id'], 'Name_L': name_l, 'Gene_L': list(genes_1),
                                 'Gene_L_ens': list(genes_ens_1), 'Receptor_L': index1['receptor_x'],
                                 'Membrane_L': index1['transmembrane_x'], 'Secretion_L': index1['secretion_x'],
                                 'Ligand_L': index1['ligand_x'], 'Adhesion_L': index1['adhesion_x'],
                                 'Unity_R': index1['multidata_2_id'], 'Name_R': name_r, 'Gene_R': gene2,
                                 'Gene_R_ens': ligand, 'Receptor_R': index1['receptor_y'],
                                 'Membrane_R': index1['transmembrane_y'], 'Secretion_R': index1['secretion_y'],
                                 'Ligand_R': index1['ligand_y'], 'Adhesion_R': index1['adhesion_y'],
                                 'Total_Mean_L': list(complexes_mean_1), 'Mean_L': list(mean_r),
                                 'Total_cells_L': total_cells_r, 'Num_cells_L': list(complexes_cells_1),
                                 'Total_Mean_R': mean_expr_l, 'Mean_R': mean_l, 'Total_cells_R': total_cells_l,
                                 'Num_cells_R': num_cells_l})
                            interaction_id1.append(index1['interaction_id'])

                    complexes_mean_3 = []
                    complexes_cells_3 = []
                    complexes_num_3 = []
                    genes_ens_3 = []
                    genes_3 = []
                    mean_l = []
                    percentage_permutation_2 = []

                    for row, index in proteins.iterrows():
                        pr = index['ensembl']
                        if (pr is not None):
                            mm = clusters_counts[cluster2]
                            total_cells_l = len(mm.columns)
                            if (pr in mm.index):
                                mean_expr = mm.loc[pr].mean()
                                num_cells = len(mm.loc[pr][mm.loc[pr] > 0])
                                complexes_mean_3.append(mean_expr)
                                complexes_cells_3.append(num_cells)
                                genes_ens_3.append(pr)
                                genes_3.append(index['gene_name'])
                                mean_l.append((mm.loc[pr][mm.loc[pr] > 0]).mean())
                                percentage_permutation_2.append(permutations_pvalue.loc[pr, cluster2_name])

                    name_r = index1['name_x']
                    name_l = index1['name_y']

                    if (index1['Complex'] == True):
                        proteins_4 = get_proteins_in_complex_composition(index1['multidata_2_id'])
                        complexes_mean_4 = []
                        complexes_cells_4 = []
                        complexes_num_4 = []
                        genes_ens_4 = []
                        genes_4 = []
                        mean_r = []

                        for row, index in proteins_4.iterrows():
                            pr = index['ensembl']
                            if (pr is not None):
                                mm2 = clusters_counts[cluster]
                                total_cells_r = len(mm2.columns)
                                if (pr in mm2.index):
                                    mean_expr_r = mm2.loc[pr].mean()
                                    num_cells_r = len(mm2.loc[pr][mm2.loc[pr] > 0])
                                    complexes_mean_4.append(mean_expr_r)
                                    if (mean_expr_r > 0):
                                        complexes_num_4.append('yes')
                                    complexes_cells_4.append(num_cells_r)
                                    genes_ens_4.append(pr)
                                    genes_4.append(index['gene_name'])
                                    mean_r.append((mm2.loc[pr][mm2.loc[pr] > 0]).mean())
                                    percentage_permutation_2.append(permutations_pvalue.loc[pr, cluster_name])

                        if (all(percentage_permutation_2) != 0):
                            cluster_mean2.append(
                                {'Unity_L': index1['multidata_2_id'], 'Name_L': name_l, 'Gene_L': list(genes_4),
                                 'Gene_L_ens': list(genes_ens_4), 'Receptor_L': index1['receptor_y'],
                                 'Membrane_L': index1['transmembrane_y'],
                                 'Secretion_L': index1['secretion_y'], 'Ligand_L': index1['ligand_y'],
                                 'Adhesion_L': index1['adhesion_y'],
                                 'Unity_R': index1['multidata_1_id'], 'Name_R': name_r, 'Gene_R': list(genes_3),
                                 'Gene_R_ens': list(genes_ens_3), 'Receptor_R': index1['receptor_x'],
                                 'Membrane_R': index1['transmembrane_x'], 'Secretion_R': index1['secretion_x'],
                                 'Ligand_R': index1['ligand_x'], 'Adhesion_R': index1['adhesion_x'],
                                 'Total_Mean_L': list(complexes_mean_4), 'Mean_L': list(mean_r),
                                 'Total_cells_L': total_cells_r, 'Num_cells_L': list(complexes_cells_4),
                                 'Total_Mean_R': list(complexes_mean_3), 'Mean_R': list(mean_l),
                                 'Total_cells_R': total_cells_l, 'Num_cells_R': list(complexes_cells_3)})
                            interaction_id2.append(index1['interaction_id'])
                    else:
                        genes_multidata = get_gene_for_multidata(index1['multidata_2_id'])
                        receptor2 = genes_multidata.iloc[0]['ensembl']
                        gene1 = genes_multidata.iloc[0]['gene_name']
                        mm1 = clusters_counts[cluster]
                        mean_expr_r = 0
                        num_cells_r = 0
                        total_cells_r = len(mm1.columns)
                        if (receptor2 in mm1.index):
                            mean_expr_r = mm1.loc[receptor2].mean()
                            num_cells_r = len(mm1.loc[receptor2][mm1.loc[receptor2] > 0])
                            mean_r = (mm1.loc[receptor2][mm1.loc[receptor2] > 0]).mean()
                            percentage_permutation_2.append(permutations_pvalue.loc[receptor2, cluster_name])

                            if (all(percentage_permutation_2) != 0):
                                cluster_mean2.append(
                                    {'Unity_L': index1['multidata_2_id'], 'Name_L': name_l, 'Gene_L': gene1,
                                     'Gene_L_ens': receptor2, 'Receptor_L': index1['receptor_y'],
                                     'Membrane_L': index1['transmembrane_y'], 'Secretion_L': index1['secretion_y'],
                                     'Ligand_L': index1['ligand_y'], 'Adhesion_L': index1['adhesion_y'],
                                     'Unity_R': index1['multidata_1_id'], 'Name_R': name_r, 'Gene_R': list(genes_3),
                                     'Gene_R_ens': list(genes_ens_3), 'Receptor_R': index1['receptor_x'],
                                     'Membrane_R': index1['transmembrane_x'], 'Secretion_R': index1['secretion_x'],
                                     'Ligand_R': index1['ligand_x'], 'Adhesion_R': index1['adhesion_x'],
                                     'Total_Mean_L': mean_expr_r, 'Mean_L': mean_r, 'Total_cells_L': total_cells_r,
                                     'Num_cells_L': num_cells_r,
                                     'Total_Mean_R': list(complexes_mean_3), 'Mean_R': list(mean_l),
                                     'Total_cells_R': total_cells_l, 'Num_cells_R': list(complexes_cells_3)})
                                interaction_id2.append(index1['interaction_id'])
                df1 = pd.DataFrame(cluster_mean1, index=interaction_id1, columns=columns)
                df2 = pd.DataFrame(cluster_mean2, index=interaction_id2, columns=columns)
                frames = [df1, df2]
                all_interactions_cluster = pd.concat(frames)
                # all_interactions_cluster.sort_values('Mean_Sum', ascending=True)
                path_out = 'out/complexes/Cluster_%s_Cluster_%s_min%d.txt' % (
                    cluster_name, cluster2_name, threshold)
                all_interactions_cluster.to_csv(path_out, sep="\t", index=False)