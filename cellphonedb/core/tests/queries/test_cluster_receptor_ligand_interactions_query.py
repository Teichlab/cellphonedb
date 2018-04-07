from unittest import TestCase

import pandas as pd

from cellphonedb.core.Cellphonedb import data_test_dir
from cellphonedb.core.queries import cluster_receptor_ligand_interactions
from utils import dataframe_functions


class TestClusterReceptorLigandInteractionsQuery(TestCase):
    FIXTURES_SUBPATH = '{}/queries'.format(data_test_dir)

    def test_receptor_ligand_call(self):
        data = self._load_fixtures()
        self._assert_cluster_receptor_ligand_call(
            data,
            'Result of Cluster Receptor Ligand Interaction Query did not match with expected',
            'Result Extended of Cluster Receptor Ligand Interaction Query did not match with expected')

    def test_receptor_ligand_call_empty_counts(self):
        data = self._load_fixtures()

        data['cluster_counts'].drop(data['cluster_counts'].index, inplace=True)
        data['result_expected'].drop(data['result_expected'].index, inplace=True)
        data['result_extended_expected'].drop(data['result_extended_expected'].index, inplace=True)

        self._assert_cluster_receptor_ligand_call(
            data, 'Result of Cluster Receptor Ligand Interaction Query Empty did not match with expected',
            'Result of Cluster Receptor Ligand Interaction Query Empty did not match with expected'
        )

    def _assert_cluster_receptor_ligand_call(self, data, result_assert_msg, result_extended_assert_msg):
        result, result_extended = cluster_receptor_ligand_interactions.call(
            data['cluster_counts'], threshold=0.2, enable_integrin=True, enable_complex=True,
            complex_composition=data['complex_composition'], genes_expanded=data['genes'],
            complex_expanded=data['complex_expanded'],
            interactions=data['interactions'], clusters_names=[])

        self.assertTrue(
            dataframe_functions.dataframes_has_same_data(result, data['result_expected'], round_decimals=True),
            result_assert_msg)
        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_extended, data['result_extended_expected']),
                        result_extended_assert_msg)

    def _load_fixtures(self):
        data = {}
        data['cluster_counts'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_cluster_counts.csv'.format(self.FIXTURES_SUBPATH))

        data['complex_composition'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        data['genes'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_gene.csv'.format(self.FIXTURES_SUBPATH))

        data['complex_expanded'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_complex.csv'.format(self.FIXTURES_SUBPATH))

        data['interactions'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_interaction.csv'.format(self.FIXTURES_SUBPATH))

        data['result_expected'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_result.csv'.format(self.FIXTURES_SUBPATH))

        data['result_extended_expected'] = pd.read_csv(
            '{}/cluster_receptor_ligand_interactions_query_result_extended.csv'.format(self.FIXTURES_SUBPATH))

        return data
