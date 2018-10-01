import os

import pandas as pd

from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.app.cellphonedb_app import output_test_dir, data_test_dir, cellphonedb_app
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher
from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase
from cellphonedb.utils import dataframe_functions


class TestTerminalMethodlAnalysis(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)

    def test_test_data(self):
        data = 'test'
        project_name = 'test_data'
        threshold = 0.1
        self._method_call(data, project_name, threshold)

    def _method_call(self, data: str, project_name: str, threshold: float):
        result_means_filename = self._get_result_filename('means', data)
        result_deconvoluted_filename = self._get_result_filename('deconvoluted', data)

        meta_filename = os.path.realpath('{}/hi_{}_meta.txt'.format(data_test_dir, data))
        counts_filename = os.path.realpath('{}/hi_{}_counts.txt'.format(data_test_dir, data))

        LocalMethodLauncher(cellphonedb_app.cellphonedb).cpdb_analysis_local_method_launcher(meta_filename,
                                                                                             counts_filename,
                                                                                             project_name,
                                                                                             threshold,
                                                                                             output_test_dir,
                                                                                             result_means_filename,
                                                                                             result_deconvoluted_filename)

        self._assert_result('means', data, project_name, result_means_filename)
        self._assert_result('deconvoluted', data, project_name, result_deconvoluted_filename)

    def _assert_result(self, namefile: str, data: str, project_name: str,
                       result_means_filename: str) -> None:
        means_test_filename = 'analysis_{}_result__data-{}.txt'.format(namefile, data)
        original_means = pd.read_table('{}/{}'.format(data_test_dir, means_test_filename))
        result_means = pd.read_table('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))
        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_means, original_means))
        self.remove_file('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))

    def _get_result_filename(self, base_name, data: str) -> str:
        base_filename = '{}__data-{}'.format(base_name, data)
        random_filename = self.get_test_filename(base_filename, 'txt')

        return random_filename
