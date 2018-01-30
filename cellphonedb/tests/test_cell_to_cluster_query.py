import os
import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.queries import cells_to_clusters
from utilities import dataframe_functions


class TestCellToClusterQuery(TestCase):
    def create_app(self):
        return create_app()

    def test_cell_to_cluster_real_data(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        meta = pd.read_csv('{}/fixtures/real_meta.csv'.format(current_dir), index_col=0)
        counts = pd.read_csv('{}/fixtures/real_counts.csv'.format(current_dir), index_col=0)

        cell_to_cluster_result = cells_to_clusters.call(counts, meta)

        cell_to_cluster_result['gene'] = cell_to_cluster_result.index

        expected_cell_to_cluster_result = pd.read_csv(
            '{}/fixtures/real_cells_to_clusters_result.csv'.format(current_dir))

        self.assertTrue(
            dataframe_functions.dataframes_has_same_data(cell_to_cluster_result, expected_cell_to_cluster_result,
                                                         'gene'),
            'Cells to cluster real result is differnet than expected')
