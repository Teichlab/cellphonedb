import os
import pandas as pd
import numpy as np
import math
import itertools
import collections
import scipy.stats
from numpy import *
import time
# import matplotlib.pyplot as plt
# import seaborn as sns


# from cellphonedb.api import create_app
import methods_refactor
from cellphonedb import extensions
# from cellphonedb.extensions import db

from cellphonedb.core.models.gene.db_model_gene import Gene
from cellphonedb.core.models.interaction.db_model_interaction import Interaction
from cellphonedb.core.models.multidata.db_model_multidata import Multidata
from cellphonedb.core.models.protein.db_model_protein import Protein
# from cellphonedb.repository import complex_repository
from cellphonedb.flask_app import create_app

current_dir = os.path.dirname(os.path.realpath(__file__))

start_time = time.time()

app = create_app()


def query_interactions():
    with app.app_context():
        ######  Interactions

        interactions_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(
            Interaction)
        all_interactions_df = pd.read_sql(interactions_query.statement,
                                          extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        ######  Genes

        genes_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Gene)
        genes_query_df = pd.read_sql(genes_query.statement,
                                     extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        ######  Proteins - multidata

        proteins_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Protein)
        multidata_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Multidata)

        proteins_df = pd.read_sql(proteins_query.statement,
                                  extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        multidata_df = pd.read_sql(multidata_query.statement,
                                   extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        proteins_multidata = pd.merge(proteins_df, multidata_df, left_on='protein_multidata_id',
                                      right_on='id_multidata')

        proteins_multidata_genes = pd.merge(proteins_multidata, genes_query_df, left_on='id_protein',
                                            right_on='protein_id')

        protein_interaction_1 = pd.merge(all_interactions_df, proteins_multidata_genes, left_on='multidata_1_id',
                                         right_on='id_multidata')
        # protein_interaction_1.rename(index=str, columns={'id': 'interaction_id'}, inplace=True)

        protein_interaction_2 = pd.merge(all_interactions_df, proteins_multidata_genes, left_on='multidata_2_id',
                                         right_on='id_multidata')
        # protein_interaction_2.rename(index=str, columns={'id': 'interaction_id'}, inplace=True)

        all_protein_interactions = pd.merge(protein_interaction_1, protein_interaction_2, left_on='id_interaction',
                                            right_on='id_interaction')
        all_protein_interactions.rename(index=str, columns={'multidata_1_id_x': 'multidata_1_id'}, inplace=True)
        all_protein_interactions.rename(index=str, columns={'multidata_2_id_x': 'multidata_2_id'}, inplace=True)
        all_protein_interactions.drop(['multidata_1_id_y'], axis=1, inplace=True)
        all_protein_interactions.drop(['multidata_2_id_y'], axis=1, inplace=True)

        receptor_membrane = all_protein_interactions[(all_protein_interactions['receptor_x'] == True) &
                                                     (all_protein_interactions['secreted_highlight_y'] == False) &
                                                     (all_protein_interactions['source_x'] == 'curated')]

        membrane_receptor = all_protein_interactions[(all_protein_interactions['receptor_y'] == True) &
                                                     (all_protein_interactions['secreted_highlight_x'] == False) &
                                                     (all_protein_interactions['source_x'] == 'curated')]

        receptor_secreted = all_protein_interactions[
            (all_protein_interactions['receptor_x'] == True) & (all_protein_interactions['other_x'] == False) &
            (all_protein_interactions['secreted_highlight_y'] == True)]
        secreted_receptor = all_protein_interactions[
            (all_protein_interactions['receptor_y'] == True) & (all_protein_interactions['other_y'] == False) &
            (all_protein_interactions['secreted_highlight_x'] == True)]

        frames = [receptor_membrane, membrane_receptor, receptor_secreted, secreted_receptor]

        all_1_1_interactions = pd.concat(frames)

        all_1_1_interactions.drop(['score_1_y'], axis=1, inplace=True)
        all_1_1_interactions.drop(['score_2_y'], axis=1, inplace=True)
        all_1_1_interactions.rename(index=str, columns={'score_1_x': 'score_1'}, inplace=True)
        all_1_1_interactions.rename(index=str, columns={'score_2_x': 'score_2'}, inplace=True)

        all_1_1_interactions = all_1_1_interactions[all_1_1_interactions['score_2'] == 1]

        all_1_1_interactions.to_csv('Neil/all_interactions.txt', index=False, sep="\t")

        ########   All interactions
        return all_1_1_interactions


all_interactions = query_interactions()
CPD_TEST = True

if CPD_TEST:
    counts = pd.read_table('Neil/test_counts.txt'.format(methods_refactor.methods_example_data), index_col=0)
    meta = pd.read_table('Neil/test_meta.txt'.format(methods_refactor.methods_example_data), index_col=0)
    data_font = 'test'
else:
    counts = pd.read_table('Neil/counts.txt'.format(methods_refactor.methods_input_data), index_col=0)
    meta = pd.read_table('Neil/metadata.txt'.format(methods_refactor.methods_input_data), index_col=0)
    data_font = 'original'



all_genes = all_interactions['ensembl_x'].tolist()
all_genes.extend(all_interactions['ensembl_y'].tolist())
genes_unique = set(all_genes)

counts_filtered = counts.loc[counts.index.isin(genes_unique)]
counts_filtered.to_csv('Neil/MIRJANAS_CODE_one_one_filtered_counts{}.txt'.format(data_font), sep="\t")

in_x = all_interactions['ensembl_x'].isin(counts_filtered.index)
all_interactions = all_interactions.loc[in_x]

in_y = all_interactions['ensembl_y'].isin(counts_filtered.index)
all_interactions = all_interactions.loc[in_y]
all_interactions.sort_values('id_interaction').to_csv(
    'Neil/MIRJANAS_CODE_filtered_interactions_{}.txt'.format(data_font), index=False,
    sep="\t")
