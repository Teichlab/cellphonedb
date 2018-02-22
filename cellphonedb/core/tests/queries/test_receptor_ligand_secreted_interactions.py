from unittest import TestCase

import pandas as pd

import cellphonedb.core.models.interaction.filter_interaction
from cellphonedb.core.Cellphonedb import data_test_dir


class TestReceptorLigandSecretedInteractions(TestCase):

    def test_get_receptor_ligand_secreted_interactions(self):
        cluster_counts = pd.read_csv('{}/secreted_interactions_cluster_counts.csv'.format(data_test_dir))
        interactions = pd.read_csv('{}/secreted_interactions_interactions.csv'.format(data_test_dir))
        expected_result = pd.read_csv('{}/secreted_interactions_enabled_interactions.csv'.format(data_test_dir))

        result = cellphonedb.core.models.interaction.filter_interaction.filter_by_receptor_ligand_secreted(
            cluster_counts, interactions)

        self.assertEqual(len(result), len(expected_result[expected_result['enabled']]))
        result_matches = True
        for index, interaction in expected_result.iterrows():
            if interaction['enabled']:
                if len(result[(interaction['id_interaction'] == result['id_interaction']) &
                              (interaction['id_multidata_receptors'] == result['id_multidata_receptors']) &
                              (interaction['id_multidata_ligands'] == result['id_multidata_ligands'])
                       ]) != 1:
                    result_matches = False

        self.assertTrue(result_matches)
