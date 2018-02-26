import os
from unittest import TestCase

import pandas as pd

from cellphonedb.app import import_config
from cellphonedb.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy
from cellphonedb.core.queries import cells_to_clusters
from utils import dataframe_functions


class TestQueryLauncher(TestCase):

    def setUp(self):
        super().setUp()
        config = import_config.AppConfig()
        cellphone_config = config.get_cellphone_config()

        self.cellphonedb = CellphonedbSqlalchemy(cellphone_config)

    def test_cell_to_cluster_real_data(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        meta = pd.read_csv('{}/fixtures/real_meta.csv'.format(current_dir), index_col=0)
        counts = pd.read_csv('{}/fixtures/real_counts.csv'.format(current_dir), index_col=0)

        genes = self.cellphonedb.database_manager.get_repository('gene').get_all()
        cell_to_cluster_result = cells_to_clusters.call(meta, counts, genes)

        cell_to_cluster_result['gene'] = cell_to_cluster_result.index

        expected_cell_to_cluster_result = pd.read_csv(
            '{}/fixtures/real_cells_to_clusters_result.csv'.format(current_dir))

        self.assertTrue(
            dataframe_functions.dataframes_has_same_data(cell_to_cluster_result, expected_cell_to_cluster_result),
            'Cells to cluster real result is differnet than expected')
