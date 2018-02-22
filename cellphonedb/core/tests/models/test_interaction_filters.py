from unittest import TestCase

import pandas as pd

from cellphonedb.core.Cellphonedb import data_test_dir
from cellphonedb.core.models.interaction import filter_interaction


class TestInteractionFilters(TestCase):
    def test_filter_by_integrin(self):
        proteins = pd.read_csv('{}/filter_interaction_integrin_proteins.csv'.format(data_test_dir))
        interactions = pd.read_csv('{}/filter_interaction_interactions.csv'.format(data_test_dir))
        expected_result = pd.read_csv('{}/filter_interaction_interactions_filtered.csv'.format(data_test_dir))

        result = filter_interaction.filter_by_receptor_ligand_integrin(proteins, interactions)

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
