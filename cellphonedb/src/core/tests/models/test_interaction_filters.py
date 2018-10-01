from unittest import TestCase

import pandas as pd

from cellphonedb.src.core.Cellphonedb import data_test_dir
from cellphonedb.src.core.models.interaction import interaction_filter
from cellphonedb.utils import dataframe_functions


class TestInteractionFilters(TestCase):
    def test_filter_by_integrin(self):
        proteins = pd.read_csv('{}/filter_interaction/filter_interaction_integrin_proteins.csv'.format(data_test_dir))
        interactions = pd.read_csv('{}/filter_interaction/filter_interaction_interactions.csv'.format(data_test_dir))
        expected_result = pd.read_csv(
            '{}/filter_interaction/filter_interaction_interactions_filtered.csv'.format(data_test_dir))

        result = interaction_filter.filter_by_receptor_ligand_integrin(proteins, interactions)

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

    def test_filter_by_multidatas(self):
        multidatas = pd.read_csv(
            '{}/filter_interaction/filter_interaction_multidatas_multidata.csv'.format(data_test_dir))
        interactions = pd.read_csv(
            '{}/filter_interaction/filter_interaction_multidatas_interaction.csv'.format(data_test_dir))

        result = interaction_filter.filter_by_multidatas(multidatas, interactions)
        expected_result = interactions[interactions['test_both_enabled']]

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))

    def test_filter_by_any_multidata(self):

        multidatas = pd.read_csv(
            '{}/filter_interaction/filter_interaction_multidatas_multidata.csv'.format(data_test_dir))
        interactions = pd.read_csv(
            '{}/filter_interaction/filter_interaction_multidatas_interaction.csv'.format(data_test_dir))

        result = interaction_filter.filter_by_any_multidatas(multidatas, interactions)
        expected_result = interactions[interactions['test_any_enabled']]

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))
