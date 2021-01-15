from unittest import TestCase

import pandas as pd

from cellphonedb.src.core.Cellphonedb import data_test_dir
from cellphonedb.src.core.models.complex import complex_helper
from cellphonedb.utils import dataframe_functions


class TestHelperComplex(TestCase):
    FIXTURES_SUBPATH = '{}/helper_complex'.format(data_test_dir)

    def test_get_involved_complex_from_protein(self):
        proteins = pd.read_csv('{}/helper_complex_protein.csv'.format(self.FIXTURES_SUBPATH), index_col=0)
        complex_composition = pd.read_csv('{}/helper_complex_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        result_expected = pd.read_csv('{}/helper_complex_result.csv'.format(self.FIXTURES_SUBPATH), index_col=3)

        result = complex_helper.get_involved_complex_composition_from_protein(proteins, complex_composition)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, result_expected))

    def test_get_involved_complex_from_protein_empty_result(self):
        proteins = pd.read_csv('{}/helper_complex_protein.csv'.format(self.FIXTURES_SUBPATH), index_col=0)
        proteins.drop(proteins.index, inplace=True)
        complex_composition = pd.read_csv('{}/helper_complex_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        result = complex_helper.get_involved_complex_composition_from_protein(proteins, complex_composition)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, pd.DataFrame(columns=['complex_multidata_id', 'protein_multidata_id', 'total_protein'])))

    def test_get_involved_complex_composition_from_protein(self):
        proteins = pd.read_csv('{}/helper_complex_protein.csv'.format(self.FIXTURES_SUBPATH), index_col=0)
        complex_composition = pd.read_csv('{}/helper_complex_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        result_expected = pd.read_csv('{}/helper_complex_result_drop_duplicates.csv'.format(self.FIXTURES_SUBPATH))

        result = complex_helper.get_involved_complex_composition_from_protein(proteins, complex_composition)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, result_expected))
