import os
import pandas as pd
import numpy as np
import math
import itertools
import collections
import scipy.stats
from numpy import *

import sys

import methods_refactor
from cellphonedb import extensions
from cellphonedb.core.models.complex.db_model_complex import Complex
from cellphonedb.core.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellphonedb.core.models.gene.db_model_gene import Gene
from cellphonedb.core.models.interaction.db_model_interaction import Interaction
from cellphonedb.core.models.multidata.db_model_multidata import Multidata
from cellphonedb.core.models.protein.db_model_protein import Protein
from utils import dataframe_format, dataframe_functions

from cellphonedb.flask_app import create_app

current_dir = os.path.dirname(os.path.realpath(__file__))

app = create_app()

CPD_TEST = True

print("[+] Launched Complexes Method with data. TESTING: {}".format('TRUE' if CPD_TEST else 'FALSE'))

if CPD_TEST:
    counts = pd.read_table('{}/test_counts.txt'.format(methods_refactor.methods_example_data), index_col=0)
    meta = pd.read_table('{}/test_meta.txt'.format(methods_refactor.methods_example_data), index_col=0)
    data_font = 'test'
else:
    counts = pd.read_table('{}/counts.txt'.format(methods_refactor.methods_input_data), index_col=0)
    meta = pd.read_table('{}/metadata.txt'.format(methods_refactor.methods_input_data), index_col=0)
    data_font = 'original'


# TODO: BUG interactions with complex multidata_2_id are not pressent.
def query_complex_interactions():
    with app.app_context():
        ######  Genes

        genes_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement,
                                     extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        genes_query_df.to_csv('cellphonedb/REFACTOR_genes_{}.txt'.format(data_font), sep="\t")
        original_genes = pd.read_table('cellphonedb/REFACTOR_genes_{}.txt'.format(data_font), index_col=0)
        assert (dataframe_functions.dataframes_has_same_data(original_genes, genes_query_df))

        ######  Proteins

        proteins_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Protein)
        proteins_df = pd.read_sql(proteins_query.statement,
                                  extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        proteins_df.to_csv('cellphonedb/REFACTOR_proteins_{}.txt'.format(data_font), sep="\t")
        original_proteins = pd.read_table('cellphonedb/REFACTOR_proteins_{}.txt'.format(data_font), index_col=0)
        assert (dataframe_functions.dataframes_has_same_data(original_proteins, proteins_df))

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
        multidata_df.to_csv('cellphonedb/REFACTOR_multidata_{}.txt'.format(data_font), sep="\t")
        original_multidata = pd.read_table('cellphonedb/REFACTOR_multidata_{}.txt'.format(data_font), index_col=0)
        assert (dataframe_functions.dataframes_has_same_data(original_multidata, multidata_df))

        complex_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Complex)
        complex_df = pd.read_sql(complex_query.statement,
                                 extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

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
        complex_composition_df.to_csv('cellphonedb/REFACTOR_complex_composition_{}.txt'.format(data_font), sep="\t")
        original_complex_composition = pd.read_table(
            'cellphonedb/REFACTOR_complex_composition_{}.txt'.format(data_font), index_col=0)
        assert (dataframe_functions.dataframes_has_same_data(original_complex_composition, complex_composition_df))

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

        interactions_complex.to_csv('Neil/REFACTOR_all_complex_interactions_{}.txt'.format(data_font), sep="\t")
        original_complex_interactions = pd.read_table('Neil/ORIGINAL_all_complex_interactions_{}.txt'.format(data_font),
                                                      index_col=0)

        assert (dataframe_functions.dataframes_has_same_data(original_complex_interactions,
                                                             interactions_complex.fillna(value=nan)))

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
        # print(complex_proteins_genes.shape)

        return gene_protein_df


all_complex_interactions = query_complex_interactions()
new_clusters = meta.cell_type.unique()

all_complex_genes = []
remove_rows = []
for complex_interaction_index, complex_interaction in all_complex_interactions.iterrows():
    proteins = get_proteins_in_complex_composition(complex_interaction['complex_multidata_id'])

    ## Check if all proteins of complex_composition are in counts
    for protein_index, protein_row in proteins.iterrows():
        pr = protein_row['ensembl']
        all_complex_genes.append(pr)
        if (pr not in counts.index):
            remove_rows.append(complex_interaction_index)

    ## Check if all proteins of complex_composition
    if (complex_interaction['Complex'] == True):
        proteins_2 = get_proteins_in_complex_composition(complex_interaction['multidata_2_id'])
        for protein_index, index in proteins_2.iterrows():
            pr = index['ensembl']
            all_complex_genes.append(pr)
            if (pr not in counts.index):
                remove_rows.append(complex_interaction_index)

    else:
        genes_multidata = get_gene_for_multidata(complex_interaction['multidata_2_id'])
        name_ens = genes_multidata.iloc[0]['ensembl']
        all_complex_genes.append(name_ens)
        if (name_ens not in counts.index):
            remove_rows.append(complex_interaction_index)

genes_unique = set(all_complex_genes)

counts_filtered = counts.loc[counts.index.isin(genes_unique)]
counts_filtered.to_csv('Neil/REFACTOR_complexes_filtered_counts_{}.txt'.format(data_font), sep="\t")

remove_rows_int = [int(i) for i in remove_rows]

all_complex_interactions_filtered = all_complex_interactions.loc[
    np.setdiff1d(all_complex_interactions.index, remove_rows_int)]

all_complex_interactions_filtered.to_csv('Neil/REFACTOR_complexes_filtered_{}.txt'.format(data_font), sep="\t")

# def assertions(path, ):
#     original = pd.read_table('Neil/ORIGINAL_all_complex_interactions_{}.txt'.format(data_font), index_col=0)
#     refactored = pd.read_table('Neil/REFACTORED_all_complex_interactions_{}.txt'.format(data_font), index_col=0)
#
#     assert (dataframe_functions.dataframes_has_same_data(original, refactored))
#
#
#
# assertions()
