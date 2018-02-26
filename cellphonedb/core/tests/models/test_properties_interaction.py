from unittest import TestCase

import pandas as pd

from cellphonedb.core.Cellphonedb import data_test_dir
from cellphonedb.core.models.interaction import properties_interaction
from utilities import dataframe_functions


class TestPropertiesInteraction(TestCase):
    def test_is_receptor_ligand(self):
        interactions = pd.read_csv('{}/properties_multidata_is_receptor_ligand.csv'.format(data_test_dir))

        correct_result_rl = True
        correct_result_lr = True

        for index, interaction in interactions.iterrows():
            if properties_interaction.is_receptor_ligand(interaction, '_1', '_2') != interaction[
                'test_is_receptor_ligand']:
                correct_result_rl = False
            if properties_interaction.is_receptor_ligand(interaction, '_2', '_1') != interaction[
                'test_is_ligand_receptor']:
                correct_result_lr = False

        self.assertTrue(correct_result_rl, 'Some receptor_ligand interactions results are not correct')
        self.assertTrue(correct_result_lr, 'Some ligand_receptor interactions results are not correct')

    def test_get_receptor_ligand_ligand_receptor(self):

        interactions = pd.read_csv(
            '{}/properties_interaction_get_receptor_ligand_ligand_receptor_interaction_extended.csv'.format(
                data_test_dir))

        result_expected = pd.read_csv(
            '{}/properties_interaction_get_receptor_ligand_ligand_receptor_result_expected.csv'.format(data_test_dir))

        result = properties_interaction.get_receptor_ligand_ligand_receptor(interactions)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_expected, result))
