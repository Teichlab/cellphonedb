import os
from typing import Optional

import pandas as pd

from cellphonedb.src.app.cellphonedb_app import output_test_dir, data_test_dir, cellphonedb_app
from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.core.utils.subsampler import Subsampler
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher
from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase
from cellphonedb.utils import dataframe_functions


class TestTerminalMethodlAnalysis(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)

    def test_non_statistical_method__data_test__threshold__01__precision_1(self):
        data = 'test'
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 1
        self._method_call(data, project_name, threshold, result_precision)

    def test_non_statistical_method__data_test__threshold__01__precision_1_hgnc(self):
        data = 'test_custom_counts_data'
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 1
        self._method_call(data, project_name, threshold, result_precision, counts_data='hgnc_symbol')

    def test_non_statistical_method__data_test__threshold__01__precision_1_gene_name(self):
        data = 'test_custom_counts_data'
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 1
        self._method_call(data, project_name, threshold, result_precision, counts_data='gene_name')

    def test_non_statistical_method__data_test__threshold__01__precision_3(self):
        data = 'test'
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 3
        self._method_call(data, project_name, threshold, result_precision)

    def test_non_statistical_method_subsampled_data_test__threshold__01__precision_3__num_pc_4__num_cells_4(self):
        data = 'test_subsampled'
        project_name = 'test_data'
        threshold = 0.1
        result_precision = 3
        subsampler = Subsampler(False, 4, 4, debug_seed=0)
        self._method_call(data, project_name, threshold, result_precision, subsampler)

    def _method_call(self, data: str, project_name: str, threshold: float, result_precision: int,
                     subsampler: Optional[Subsampler] = None, counts_data: str = 'ensembl'):
        result_names_as_fixture = False
        if result_names_as_fixture:
            result_deconvoluted_filename, result_means_filename, result_significant_means_filename = self._original_names(
                data, result_precision, threshold)
        else:
            result_means_filename = self._get_result_filename('means', data, threshold, result_precision)
            result_significant_means_filename = self._get_result_filename('significant_means', data, threshold,
                                                                          result_precision)
            result_deconvoluted_filename = self._get_result_filename('deconvoluted', data, threshold, result_precision)

        meta_filename = os.path.realpath('{}/hi_{}_meta.txt'.format(data_test_dir, data))

        if counts_data == 'ensembl':
            counts_file = '{}/hi_{}_counts.txt'.format(data_test_dir, data)
        else:
            counts_file = '{}/hi_{}_counts_{}.txt'.format(data_test_dir, data, counts_data)

        counts_filename = os.path.realpath(counts_file)

        LocalMethodLauncher(cellphonedb_app.cellphonedb).cpdb_analysis_local_method_launcher(meta_filename,
                                                                                             counts_filename,
                                                                                             counts_data,
                                                                                             project_name,
                                                                                             threshold,
                                                                                             output_test_dir,
                                                                                             'txt',
                                                                                             result_means_filename,
                                                                                             result_significant_means_filename,
                                                                                             result_deconvoluted_filename,
                                                                                             result_precision,
                                                                                             subsampler
                                                                                             )

        self._assert_result('means', data, project_name, result_means_filename, threshold, result_precision)
        self._assert_result('significant_means', data, project_name, result_significant_means_filename, threshold,
                            result_precision)
        self._assert_result('deconvoluted', data, project_name, result_deconvoluted_filename, threshold,
                            result_precision)

    def _original_names(self, data, result_precision, threshold):
        str_threshold = ''.join(str(threshold).split('.'))

        result_means_filename = 'analysis__{}_result__data-{}_threshold-{}_precision-{}.txt'.format('means',
                                                                                                    data,
                                                                                                    str_threshold,
                                                                                                    result_precision)
        result_significant_means_filename = 'analysis__{}_result__data-{}_threshold-{}_precision-{}.txt'.format(
            'significant_means',
            data,
            str_threshold,
            result_precision)
        result_deconvoluted_filename = 'analysis__{}_result__data-{}_threshold-{}_precision-{}.txt'.format(
            'deconvoluted',
            data,
            str_threshold,
            result_precision)
        return result_deconvoluted_filename, result_means_filename, result_significant_means_filename

    def _assert_result(self,
                       namefile: str,
                       data: str,
                       project_name: str,
                       result_means_filename: str,
                       threshold: float,
                       result_precision: int,
                       ) -> None:
        str_threshold = ''.join(str(threshold).split('.'))
        test_filename = 'analysis__{}_result__data-{}_threshold-{}_precision-{}.txt'.format(namefile,
                                                                                            data,
                                                                                            str_threshold,
                                                                                            result_precision)
        original_means = pd.read_table('{}/{}'.format(data_test_dir, test_filename))
        result_means = pd.read_table('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))
        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_means, original_means))
        self.remove_file('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))

    def _get_result_filename(self, base_name, data: str, threshold: float, precision: int) -> str:
        str_threshold = ''.join(str(threshold).split('.'))
        base_filename = '{}__data-{}_threshold-{}_precision-{}'.format(base_name, data, str_threshold, precision)
        random_filename = self.get_test_filename(base_filename, 'txt')

        return random_filename
