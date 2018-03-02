from unittest import TestCase

import pandas as pd

from cellphonedb.core.Cellphonedb import data_test_dir
from cellphonedb.core.queries import query_utils
from utils import dataframe_functions


class TestQueryUtils(TestCase):
    FIXTURES_UTILS_PATH = '{}/utils'.format(data_test_dir)

    def test_apply_threshold(self):
        cluster_counts = pd.read_csv('{}/query_utils_threshold_cluster_counts.csv'.format(self.FIXTURES_UTILS_PATH))
        expected_result = pd.read_csv('{}/query_utils_threshold_results.csv'.format(self.FIXTURES_UTILS_PATH))

        gene_column_name = 'gene'

        cluster_names = list(cluster_counts.columns.values)
        cluster_names.remove(gene_column_name)

        result = query_utils.apply_threshold(cluster_counts, cluster_names, threshold=0.2)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))
