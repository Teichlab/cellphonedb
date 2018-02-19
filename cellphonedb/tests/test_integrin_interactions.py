from unittest import TestCase

import os
import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction


class IntegrinInteractions(TestCase):
    def test_integrin_filter(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        proteins = pd.read_csv('{}/fixtures/integrin_proteins.csv'.format(current_dir))
        interactions = pd.read_csv('{}/fixtures/integrin_interactions.csv'.format(current_dir))
        test_results = pd.read_csv('{}/fixtures/integrin_enabled_interactions.csv'.format(current_dir))

        filtered_interactions = filter_interaction._filter_by_integrin(proteins, interactions)

        disabled_interactions = filtered_interactions[filtered_interactions['test_enabled_interactions'] == False]

        self.assertEqual(0, len(disabled_interactions), 'There are some disabled interactions in the result')

        same_results = pd.merge(test_results, filtered_interactions,
                                on=['id_interaction', 'id_multidata_ligands', 'id_multidata_receptors'], indicator=True,
                                how='outer')

        different_results = same_results[same_results['_merge'] != 'both']

        self.assertEqual(0, len(different_results), 'some results are different')
