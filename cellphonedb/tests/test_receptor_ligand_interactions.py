import os
import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.queries import receptor_ligands_interactions
from utilities import dataframe_functions


class ReceptorLigandInteractions(TestCase):
    def create_app(self):
        return create_app()

    def test_query_01_no_integrin(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        cluster_counts = pd.read_csv('{}/fixtures/real_cells_to_clusters.csv'.format(current_dir), index_col=0)

        result_interactions, result_interactions_extended = receptor_ligands_interactions.call(cluster_counts, 0.1,
                                                                                               False)

        expected_result_interactions = pd.read_csv(
            '{}/fixtures/real_receptor_ligand_interactions_query_result.csv'.format(current_dir))

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_interactions, expected_result_interactions,
                                                                     'id_interaction'))