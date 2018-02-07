import os
import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.queries import receptor_ligands_interactions
from utilities import dataframe_functions


class ReceptorLigandInteractionsQuery(TestCase):
    def create_app(self):
        return create_app()

    def test_threshold_01_no_integrin_with_complex(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        cluster_counts = pd.read_csv('{}/fixtures/real_cells_to_clusters.csv'.format(current_dir), index_col=0)

        result_interactions, result_interactions_extended = receptor_ligands_interactions.call(cluster_counts, 0.1,
                                                                                               enable_integrin=False,
                                                                                               enable_complex=True)

        expected_result_interactions = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_query_result_no_integrin.csv'.format(current_dir))
        expected_result_interactions_extended = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_extended_query_result_no_integrin.csv'.format(current_dir))

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions, expected_result_interactions,
                                                                     'id_interaction'),
                        'Receptor Ligand non integrin result is differnet than expected')

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions_extended,
                                                                     expected_result_interactions_extended,
                                                                     'id_interaction'),
                        'Receptor Ligand extended non integrin result is differnet than expected')

    def test_threshold_01_with_integrin_and_complex(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        cluster_counts = pd.read_csv('{}/fixtures/real_cells_to_clusters.csv'.format(current_dir), index_col=0)

        result_interactions, result_interactions_extended = receptor_ligands_interactions.call(cluster_counts, 0.1,
                                                                                               enable_integrin=True,
                                                                                               enable_complex=True)

        expected_result_interactions = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_query_result_with_integrin.csv'.format(current_dir))
        expected_result_interactions_extended = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_extended_query_result_with_integrin.csv'.format(current_dir))

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions, expected_result_interactions,
                                                                     'id_interaction'),
                        'Receptor Ligand with integrin result is differnet than expected')

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions_extended,
                                                                     expected_result_interactions_extended,
                                                                     'id_interaction'),
                        'Receptor Ligand extended with integrin result is differnet than expected')
