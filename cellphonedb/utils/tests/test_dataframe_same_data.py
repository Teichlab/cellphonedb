from unittest import TestCase

import pandas as pd

from cellphonedb.utils import dataframe_functions


class TestDataframeSameData(TestCase):
    def test_compare_empty(self):
        self.assertTrue(dataframe_functions.dataframes_has_same_data(pd.DataFrame(), pd.DataFrame()))

    def test_equal(self):
        dataframe1 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        dataframe2 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        self.assertTrue(dataframe_functions.dataframes_has_same_data(dataframe1, dataframe2))

    def test_different(self):
        dataframe1 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        dataframe2 = pd.DataFrame({'col1': [5, 2], 'col2': [3, 4]})

        self.assertFalse(dataframe_functions.dataframes_has_same_data(dataframe1, dataframe2))

    def test_equal_unsorted(self):
        dataframe1 = pd.DataFrame({'col1': [2, 1], 'col2': [4, 3]})
        dataframe2 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        self.assertTrue(dataframe_functions.dataframes_has_same_data(dataframe1, dataframe2))

    def test_different_unsorted(self):
        dataframe1 = pd.DataFrame({'col1': [2, 1], 'col2': [4, 5]})
        dataframe2 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        self.assertFalse(dataframe_functions.dataframes_has_same_data(dataframe1, dataframe2))

    def test_equal_unsorted_columns(self):
        dataframe1 = pd.DataFrame({'col2': [3, 4], 'col1': [1, 2]})
        dataframe2 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        self.assertTrue(dataframe_functions.dataframes_has_same_data(dataframe1, dataframe2))

    def test_different_unsorted_columns(self):
        dataframe1 = pd.DataFrame({'col2': [3, 4], 'col1': [1, 2]})
        dataframe2 = pd.DataFrame({'col1': [1, 2], 'col2': [3, 5]})

        self.assertFalse(dataframe_functions.dataframes_has_same_data(dataframe1, dataframe2))
