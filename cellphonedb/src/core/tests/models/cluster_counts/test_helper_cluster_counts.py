from unittest import TestCase

import pandas as pd

from cellphonedb.src.core.Cellphonedb import data_test_dir
from cellphonedb.src.core.models.cluster_counts import cluster_counts_helper
from cellphonedb.utils import dataframe_functions


class TestHelperClusterCounts(TestCase):
    FIXTURES_SUBPATH = '{}/cluster_counts_model'.format(data_test_dir)

    def test_apply_threshold(self):
        cluster_counts = pd.read_csv('{}/cluster_counts_generic_cluster_counts.csv'.format(self.FIXTURES_SUBPATH))
        expected_result = pd.read_csv('{}/cluster_counts_helper_threshold_results.csv'.format(self.FIXTURES_SUBPATH))

        gene_column_name = 'gene'

        cluster_names = list(cluster_counts.columns.values)
        cluster_names.remove(gene_column_name)

        result = cluster_counts_helper.apply_threshold(cluster_counts, cluster_names, threshold=0.2)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))

    def test_merge_complex_cluster_counts(self):
        complex_counts_composition = pd.read_csv(
            '{}/cluster_counts_helper_merge_complex_cluster_counts_complex_counts_composition.csv'.format(
                self.FIXTURES_SUBPATH))

        expected_result = pd.read_csv(
            '{}/cluster_counts_helper_merge_complex_cluster_counts_result.csv'.format(
                self.FIXTURES_SUBPATH))
        cluster_names = ['cluster_1', 'cluster_2', 'cluster_3']
        complex_column_names = ['complex_multidata_id']

        result = cluster_counts_helper.merge_complex_counts(cluster_names, complex_counts_composition,
                                                            complex_column_names)

        # Need to set equal 1 to 1.0000
        result[complex_column_names] = result[complex_column_names].astype(dtype='int32')
        expected_result[complex_column_names] = expected_result[complex_column_names].astype(dtype='int32')

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))

    def test_merge_complex_cluster_counts_empty(self):
        complex_counts_composition = pd.read_csv(
            '{}/cluster_counts_helper_merge_complex_cluster_counts_complex_counts_composition.csv'.format(
                self.FIXTURES_SUBPATH))

        complex_counts_composition.drop(complex_counts_composition.index, inplace=True)
        cluster_names = ['cluster_1', 'cluster_2', 'cluster_3']
        complex_column_names = ['complex_multidata_id']

        result = cluster_counts_helper.merge_complex_counts(cluster_names, complex_counts_composition,
                                                            complex_column_names)

        self.assertTrue(result.empty)

    def test_get_complex_involved_in_counts(self):
        multidatas_counts = pd.read_csv(
            '{}/helper_cluster_counts.csv'.format(
                self.FIXTURES_SUBPATH))
        cluster_names = ['cluster_1', 'cluster_2', 'cluster_3']
        complex_composition = pd.read_csv(
            '{}/helper_cluster_counts_complex_composition.csv'.format(
                self.FIXTURES_SUBPATH))
        complex_expanded = pd.read_csv(
            '{}/helper_cluster_counts_complex.csv'.format(
                self.FIXTURES_SUBPATH))

        result_expected = pd.read_csv(
            '{}/cluster_counts_helper_get_complex_involved_in_counts_result.csv'.format(self.FIXTURES_SUBPATH))

        result = cluster_counts_helper.get_complex_involved_in_counts(multidatas_counts, cluster_names,
                                                                      complex_composition, complex_expanded)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, result_expected),
                        'get_complex_involved_in_counts result did not match with expected')
