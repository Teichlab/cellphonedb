from unittest import TestCase

import pandas as pd

from cellphonedb.src.core.Cellphonedb import data_test_dir
from cellphonedb.src.core.models.complex import complex_helper
from cellphonedb.utils import dataframe_functions


class TestHelperComplex(TestCase):
    FIXTURES_SUBPATH = '{}/helper_complex'.format(data_test_dir)

    def test_get_involved_complex_from_protein(self):
        proteins = pd.read_csv('{}/helper_complex_protein.csv'.format(self.FIXTURES_SUBPATH))
        complexes = pd.read_csv('{}/helper_complex_complex.csv'.format(self.FIXTURES_SUBPATH))
        complex_composition = pd.read_csv('{}/helper_complex_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        result_expected = pd.read_csv('{}/helper_complex_result.csv'.format(self.FIXTURES_SUBPATH))

        result = complex_helper.get_involved_complex_from_protein(proteins, complexes, complex_composition,
                                                                  drop_duplicates=False)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, result_expected))

    def test_get_involved_complex_from_protein_empty_result(self):
        proteins = pd.read_csv('{}/helper_complex_protein.csv'.format(self.FIXTURES_SUBPATH))
        proteins.drop(proteins.index, inplace=True)
        complexes = pd.read_csv('{}/helper_complex_complex.csv'.format(self.FIXTURES_SUBPATH))
        complex_composition = pd.read_csv('{}/helper_complex_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        result = complex_helper.get_involved_complex_from_protein(proteins, complexes, complex_composition,
                                                                  drop_duplicates=False)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, pd.DataFrame()))

    def test_get_involved_complex_from_protein_drop_duplicates(self):
        proteins = pd.read_csv('{}/helper_complex_protein.csv'.format(self.FIXTURES_SUBPATH))
        complexes = pd.read_csv('{}/helper_complex_complex.csv'.format(self.FIXTURES_SUBPATH))
        complex_composition = pd.read_csv('{}/helper_complex_complex_composition.csv'.format(self.FIXTURES_SUBPATH))

        result_expected = pd.read_csv('{}/helper_complex_result_drop_duplicates.csv'.format(self.FIXTURES_SUBPATH))

        result = complex_helper.get_involved_complex_from_protein(proteins, complexes, complex_composition,
                                                                  drop_duplicates=True)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, result_expected))
