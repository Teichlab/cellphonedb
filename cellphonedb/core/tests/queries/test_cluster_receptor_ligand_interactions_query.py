from unittest import TestCase

import pandas as pd

from cellphonedb.core.Cellphonedb import data_test_dir
from cellphonedb.core.queries import cluster_receptor_ligand_interactions
from utils import dataframe_functions


class TestClusterReceptorLigandInteractionsQuery(TestCase):
    FIXTURES_SUBPATH = '{}/queries'.format(data_test_dir)

    def test_receptor_ligand_call(self):
        cluster_counts = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_cluster_counts.csv'.format(self.FIXTURES_SUBPATH),
            index_col=0)
        complex_composition = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_complex_composition.csv'.format(self.FIXTURES_SUBPATH))
        genes = pd.read_csv('{}/cluster_receptor_ligand_interactions_query_gene.csv'.format(self.FIXTURES_SUBPATH))
        complex_expanded = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_complex.csv'.format(self.FIXTURES_SUBPATH))
        interacions_expanded = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_interaction.csv'.format(self.FIXTURES_SUBPATH))

        result_expected = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_result.csv'.format(self.FIXTURES_SUBPATH))

        result_extended_expected = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_result_extended.csv'.format(self.FIXTURES_SUBPATH))

        result, result_extended = cluster_receptor_ligand_interactions.call(
            cluster_counts, threshold=0.2, enable_integrin=True, enable_complex=True,
            complex_composition=complex_composition, genes_expanded=genes, complex_expanded=complex_expanded,
            interactions_expanded=interacions_expanded, clusters_names=[])

        print(result)
        print(result_expected)
        self.assertTrue(
            dataframe_functions.dataframes_has_same_data(result, result_expected, round_decimals=True),
            'Result of Cluster Receptor Ligand Interaction Query did not match with expected')
        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_extended, result_extended_expected),
                        'Result Extended of Cluster Receptor Ligand Interaction Query did not match with expected')
