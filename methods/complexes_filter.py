import os
import pandas as pd
import numpy as np
import math
import itertools
import collections
import scipy.stats
from numpy import *

import sys

from cellphonedb import extensions
from cellphonedb.core.models.complex.db_model_complex import Complex
from cellphonedb.core.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellphonedb.core.models.gene.db_model_gene import Gene
from cellphonedb.core.models.interaction.db_model_interaction import Interaction
from cellphonedb.core.models.multidata.db_model_multidata import Multidata
from cellphonedb.core.models.protein.db_model_protein import Protein
from utils import dataframe_format

from cellphonedb.flask_app import create_app

current_dir = os.path.dirname(os.path.realpath(__file__))

app = create_app()


def query_complex_interactions():
    with app.app_context():
        ######  Genes

        genes_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement,
                                     extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        genes_query_df.to_csv('cellphonedb/genes.txt', sep="\t")

        ######  Proteins

        proteins_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Protein)
        proteins_df = pd.read_sql(proteins_query.statement,
                                  extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        proteins_df.to_csv('cellphonedb/proteins.txt', sep="\t")

        proteins_genes = pd.merge(proteins_df, genes_query_df, left_on='id_protein',
                                  right_on='protein_id')

        ######  Interactions

        interactions_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(
            Interaction)
        all_interactions_df = pd.read_sql(interactions_query.statement,
                                          extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        ######  Multidata

        multidata_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Multidata)
        multidata_df = pd.read_sql(multidata_query.statement,
                                   extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        multidata_df.to_csv('cellphonedb/multidata.txt', sep="\t")
        complex_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Complex)
        complex_df = pd.read_sql(complex_query.statement,
                                 extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        # complex_unity_df.to_csv('out/complex_multidata.csv', sep="\t")

        complex_interactions_1_df = pd.merge(complex_df, all_interactions_df, left_on='complex_multidata_id',
                                             right_on='multidata_1_id')
        complex_interactions_2_df = pd.merge(complex_df, all_interactions_df, left_on='complex_multidata_id',
                                             right_on='multidata_2_id')

        complex_interactions_1_multidata_df = pd.merge(complex_interactions_1_df, multidata_df,
                                                       left_on='complex_multidata_id', right_on='id_multidata')

        complex_composition_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(
            ComplexComposition)
        complex_composition_df = pd.read_sql(complex_composition_query.statement,
                                             extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        complex_composition_df.to_csv('cellphonedb/complex_composition.txt', sep="\t")

        interactions_1_multidata_df = pd.merge(complex_interactions_1_multidata_df, multidata_df,
                                               left_on='multidata_2_id', right_on='id_multidata')
        complexes = [False] * len(interactions_1_multidata_df.index)
        interactions_1_multidata_df['Complex'] = complexes
        interactions_1_multidata_df.loc[interactions_1_multidata_df['multidata_2_id'].isin(
            complex_composition_df['complex_multidata_id']), 'Complex'] = True
        all_complex_interactions = interactions_1_multidata_df

        interactions_complex = all_complex_interactions[
            (all_complex_interactions['integrin_interaction_x'] == False) & (
                    all_complex_interactions['integrin_interaction_y'] == False)]

        interactions_complex.to_csv('Neil/all_complex_interactions.txt', sep="\t")

        return interactions_complex


def get_proteins_in_complex_composition(complex):
    with app.app_context():
        ######  Genes

        genes_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement,
                                     extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        ######  Proteins - multidata

        multidata_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Multidata)
        multidata_df = pd.read_sql(multidata_query.statement,
                                   extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        complex_composition_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(
            ComplexComposition).filter(
            ComplexComposition.complex_multidata_id == complex)
        complex_composition_df = pd.read_sql(complex_composition_query.statement,
                                             extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        proteins_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Protein)
        proteins_query_df = pd.read_sql(proteins_query.statement,
                                        extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        complex_proteins = pd.merge(complex_composition_df, proteins_query_df, left_on='protein_multidata_id',
                                    right_on='protein_multidata_id')

        complex_proteins_genes = pd.merge(complex_proteins, genes_query_df, left_on='id_protein',
                                          right_on='protein_id')

        return complex_proteins_genes


def get_gene_for_multidata(multidata_id):
    with app.app_context():
        gene_protein_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(
            Gene.ensembl, Gene.gene_name).join(Protein).filter(Protein.protein_multidata_id == multidata_id)
        gene_protein_df = pd.read_sql(gene_protein_query.statement,
                                      extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        # gene_protein_df.to_csv('out/test2.csv', index=multidata_id)
        # print(complex_proteins_genes.shape)

        return gene_protein_df


all_complex_interactions = query_complex_interactions()

counts = pd.read_table('in/counts.txt', index_col=0)
meta = pd.read_table('in/metadata.txt', index_col=0)

new_clusters = meta.cell_type.unique()

all_complex_genes = []
remove_rows = []
for row1, index1 in all_complex_interactions.iterrows():
    proteins = get_proteins_in_complex_composition(index1['complex_multidata_id'])
    for row, index in proteins.iterrows():
        pr = index['ensembl']
        all_complex_genes.append(pr)
        if (pr not in counts.index):
            remove_rows.append(row1)
    if (index1['Complex'] == True):
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
counts_filtered.to_csv('Neil/complexes_filtered_counts.txt', sep="\t")

remove_rows_int = [int(i) for i in remove_rows]

all_complex_interactions_filtered = all_complex_interactions.loc[
    np.setdiff1d(all_complex_interactions.index, remove_rows_int)]

all_complex_interactions_filtered.to_csv('Neil/complexes_filtered.txt', sep="\t")
