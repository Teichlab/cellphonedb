from unittest import TestCase

import pandas as pd

from cellphonedb.src.core.Cellphonedb import data_test_dir
from cellphonedb.src.core.models.cluster_counts import cluster_counts_filter
from cellphonedb.utils import dataframe_functions


class TestFilterClusterCounts(TestCase):
    FIXTURES_SUBPATH = '{}/cluster_counts_model'.format(data_test_dir)

    def test_filter_empty_cluster_counts(self):
        cluster_counts = pd.read_csv('{}/cluster_counts_generic_cluster_counts.csv'.format(self.FIXTURES_SUBPATH))
        expected_result = pd.read_csv(
            '{}/cluster_counts_filter_empty_cluster_results.csv'.format(self.FIXTURES_SUBPATH))

        gene_column_name = 'gene'

        cluster_names = list(cluster_counts.columns.values)
        cluster_names.remove(gene_column_name)

        result = cluster_counts_filter.filter_empty_cluster_counts(
            cluster_counts, cluster_names)

        self.assertTrue(dataframe_functions.dataframes_has_same_data(result, expected_result))
