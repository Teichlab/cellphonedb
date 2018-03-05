from unittest import TestCase

import pandas as pd

import cellphonedb.core.models.cluster_counts.filter_cluster_counts
import cellphonedb.core.models.cluster_counts.helper_cluster_counts
from cellphonedb.core.Cellphonedb import data_test_dir
from utils import dataframe_functions


class TestHelperClusterCounts(TestCase):
    FIXTURES_UTILS_PATH = '{}/cluster_counts_helper'.format(data_test_dir)

    def test_apply_threshold(self):
        cluster_counts = pd.read_csv('{}/cluster_counts_generic_cluster_counts.csv'.format(self.FIXTURES_UTILS_PATH))
        expected_result = pd.read_csv('{}/cluster_counts_helper_threshold_results.csv'.format(self.FIXTURES_UTILS_PATH))

        gene_column_name = 'gene'

        cluster_names = list(cluster_counts.columns.values)
        cluster_names.remove(gene_column_name)

        result = cellphonedb.core.models.cluster_counts.helper_cluster_counts.apply_threshold(cluster_counts,
                                                                                              cluster_names,
                                                                                              threshold=0.2)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))

    def test_filter_empty_cluster_counts(self):
        cluster_counts = pd.read_csv('{}/cluster_counts_generic_cluster_counts.csv'.format(self.FIXTURES_UTILS_PATH))
        expected_result = pd.read_csv(
            '{}/cluster_counts_filter_empty_cluster_results.csv'.format(self.FIXTURES_UTILS_PATH))

        gene_column_name = 'gene'

        cluster_names = list(cluster_counts.columns.values)
        cluster_names.remove(gene_column_name)

        result = cellphonedb.core.models.cluster_counts.filter_cluster_counts.filter_empty_cluster_counts(
            cluster_counts, cluster_names)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))
