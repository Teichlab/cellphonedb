import os
from unittest import TestCase

import pandas as pd

from cellphonedb.app import import_config
from cellphonedb.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy
from utilities import dataframe_functions


class ReceptorLigandInteractionsQuery(TestCase):
    def setUp(self):
        super().setUp()
        config = import_config.AppConfig()
        cellphone_config = config.get_cellphone_config()

        self.cellphonedb = CellphonedbSqlalchemy(cellphone_config)

    def test_threshold_01_no_integrin_with_complex(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        cluster_counts = pd.read_csv('{}/fixtures/real_cells_to_clusters.csv'.format(current_dir), index_col=0)

        result_interactions, result_interactions_extended = self.cellphonedb.query.receptor_ligands_interactions(
            cluster_counts, 0.1, enable_integrin=False, enable_complex=True, clusters_names=[])

        expected_result_interactions = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_query_result_no_integrin.csv'.format(current_dir))
        expected_result_interactions_extended = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_extended_query_result_no_integrin.csv'.format(current_dir))

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions, expected_result_interactions),
                        'Receptor Ligand non integrin result is differnet than expected')

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions_extended,
                                                                     expected_result_interactions_extended),
                        'Receptor Ligand extended non integrin result is differnet than expected')

    def test_threshold_01_with_integrin_and_complex(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        cluster_counts = pd.read_csv('{}/fixtures/real_cells_to_clusters.csv'.format(current_dir), index_col=0)

        result_interactions, result_interactions_extended = self.cellphonedb.query.receptor_ligands_interactions(
            cluster_counts, 0.1, enable_integrin=True, enable_complex=True, clusters_names=[])

        expected_result_interactions = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_query_result_with_integrin.csv'.format(current_dir))
        expected_result_interactions_extended = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_extended_query_result_with_integrin.csv'.format(current_dir))

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions, expected_result_interactions),
                        'Receptor Ligand with integrin result is differnet than expected')

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions_extended,
                                                                     expected_result_interactions_extended),
                        'Receptor Ligand extended with integrin result is differnet than expected')
