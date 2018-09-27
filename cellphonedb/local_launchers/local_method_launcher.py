import os
import pandas as pd

from cellphonedb.app.app_logger import app_logger
from cellphonedb.app.cellphonedb_app import output_dir, query_input_dir
from utils import utils


class LocalMethodLauncher(object):
    def __init__(self, cellphonedb_app):

        self.cellphonedb_app = cellphonedb_app

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            app_logger.info('Launching Method {}'.format(name))

        return method

    def cluster_statistical_analysis(self, meta_filename: str,
                                     counts_filename: str,
                                     project_name: str = '',
                                     iterations: str = '1000',
                                     threshold: float = 0.1,
                                     data_path='',
                                     output_path: str = '',
                                     means_filename: str = 'means.txt',
                                     pvalues_filename: str = 'pvalues.txt',
                                     significant_mean_filename: str = 'significant_means.txt',
                                     means_pvalues_filename: str = 'pvalues_means.txt',
                                     deconvoluted_filename='deconvoluted.txt',
                                     debug_seed: str = '-1',
                                     threads: int = -1):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir
        if project_name:
            output_path = '{}/{}'.format(output_path, project_name)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

        if LocalMethodLauncher._path_is_empty(output_path):
            app_logger.warning(
                'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))

        debug_seed = int(debug_seed)
        iterations = int(iterations)
        threads = int(threads)

        meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_filename), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_filename), index_column_first=True)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]

        pvalues_simple, means_simple, significant_means_simple, means_pvalues_simple, deconvoluted_simple = self.cellphonedb_app.method.cluster_statistical_analysis_launcher(
            meta, counts, iterations, threshold, threads, debug_seed)

        means_simple.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues_simple.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means_simple.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues_simple.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted_simple.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    def cluster_statistical_analysis_simple(self, meta_filename: str, counts_filename: str, iterations: str = '1000',
                                            data_path='', output_path: str = '', means_filename: str = 'means.txt',
                                            pvalues_filename: str = 'pvalues.txt',
                                            significant_mean_filename: str = 'significant_means.txt',
                                            means_pvalues_filename: str = 'pvalues_means.txt',
                                            deconvoluted_filename='deconvoluted.txt',
                                            debug_seed: str = '-1'):

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        debug_seed = int(debug_seed)
        iterations = int(iterations)

        meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_filename), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_filename), index_column_first=True)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]

        pvalues, means, significant_means, means_pvalues, deconvoluted = self.cellphonedb_app.cellphonedb.method.cluster_statistical_analysis_simple_launcher(
            meta, counts, iterations, debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    def cluster_statistical_analysis_complex(self, meta_filename: str, counts_filename: str, iterations: str = '1000',
                                             data_path='',
                                             output_path: str = '', means_filename: str = 'means.txt',
                                             pvalues_filename: str = 'pvalues.txt',
                                             significant_mean_filename: str = 'significant_means.txt',
                                             means_pvalues_filename: str = 'pvalues_means.txt',
                                             deconvoluted_filename='deconvoluted.txt',
                                             debug_seed: str = '-1'):

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        debug_seed = int(debug_seed)
        iterations = int(iterations)

        meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_filename), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_filename), index_column_first=True)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]

        pvalues, means, significant_means, means_pvalues, deconvoluted = self.cellphonedb_app.cellphonedb.method.cluster_statistical_analysis_complex_launcher(
            meta, counts, iterations, debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    def cpdb_method_analysis_local_launcher(self, meta_filename: str,
                                            counts_filename: str,
                                            project_name: str = '',
                                            threshold: float = 0.1,
                                            data_path='',
                                            output_path: str = '',
                                            means_filename: str = 'means.txt',
                                            deconvoluted_filename='deconvoluted.txt',
                                            debug_seed: str = '-1',
                                            threads: int = -1):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir
        if project_name:
            output_path = '{}/{}'.format(output_path, project_name)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

        if LocalMethodLauncher._path_is_empty(output_path):
            app_logger.warning(
                'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))

        debug_seed = int(debug_seed)
        threads = int(threads)

        meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_filename), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_filename), index_column_first=True)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]

        means, deconvoluted = self.cellphonedb_app.method.cpdb_method_analysis_launcher(
            meta, counts, threshold, threads, debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        deconvoluted.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    @staticmethod
    def _path_is_empty(path):
        return bool([f for f in os.listdir(path) if not f.startswith('.')])
