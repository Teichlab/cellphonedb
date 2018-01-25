from unittest import TestCase

import pandas as pd

from cellphonedb.models.interaction import filter_interaction


class IntegrinInteractions(TestCase):
    def test_asd(self):
        proteins = pd.read_csv('fixtures/integrin_proteins.csv')
        interactions = pd.read_csv('fixtures/integrin_interactions.csv')
        test_results = pd.read_csv('fixtures/integrin_enabled_interactions.csv')

        filtered_interactions = filter_interaction._filter_by_integrin(proteins, interactions)

        disabled_interactions = filtered_interactions[filtered_interactions['test_enabled_interactions'] == False]

        self.assertEqual(0, len(disabled_interactions), 'There are some disabled interactions in the result')

        same_results = pd.merge(test_results, filtered_interactions,
                                on=['id_interaction', 'id_multidata_ligands', 'id_multidata_receptors'], indicator=True,
                                how='outer')

        different_results = same_results[same_results['_merge'] != 'both']

        self.assertEqual(0, len(different_results), 'some results are different')
