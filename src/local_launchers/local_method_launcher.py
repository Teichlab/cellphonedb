import os
import pandas as pd

from src.app.app_logger import app_logger
from src.app.cellphonedb_app import output_dir, query_input_dir
from src.cpdb_exceptions.ReadFileException import ReadFileException
from utils import utils


class LocalMethodLauncher(object):
    def __init__(self, cellphonedb_app):

        self.cellphonedb_app = cellphonedb_app

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            app_logger.info('Launching Method {}'.format(name))

        return method

    def cpdb_statistical_analysis_local_method_launcher(self, meta_filename: str,
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
        data_path, output_path = self._set_paths(data_path, output_path, project_name)

        debug_seed = int(debug_seed)
        iterations = int(iterations)
        threads = int(threads)

        counts, meta = self._load_meta_counts(counts_filename, data_path, meta_filename)

        pvalues_simple, means_simple, significant_means_simple, means_pvalues_simple, deconvoluted_simple = self.cellphonedb_app.method.cpdb_statistical_analysis_launcher(
            meta, counts, iterations, threshold, threads, debug_seed)

        means_simple.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues_simple.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means_simple.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues_simple.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted_simple.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    def cpdb_analysis_local_method_launcher(self, meta_filename: str,
                                            counts_filename: str,
                                            project_name: str = '',
                                            threshold: float = 0.1,
                                            data_path='',
                                            output_path: str = '',
                                            means_filename: str = 'means.txt',
                                            deconvoluted_filename='deconvoluted.txt'
                                            ):
        data_path, output_path = self._set_paths(data_path, output_path, project_name)

        counts, meta = self._load_meta_counts(counts_filename, data_path, meta_filename)

        means, deconvoluted = self.cellphonedb_app.method.cpdb_method_analysis_launcher(
            meta, counts, threshold)

        means.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        deconvoluted.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    @staticmethod
    def _path_is_empty(path):
        return bool([f for f in os.listdir(path) if not f.startswith('.')])

    @staticmethod
    def _set_paths(data_path, output_path, project_name):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir
        if project_name:
            output_path = '{}/{}'.format(output_path, project_name)
        os.makedirs(output_path, exist_ok=True)
        if LocalMethodLauncher._path_is_empty(output_path):
            app_logger.warning(
                'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))
        return data_path, output_path

    @staticmethod
    def _load_meta_counts(counts_filename, data_path, meta_filename):
        try:
            meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_filename),
                                                       index_column_first=True)
            counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_filename),
                                                     index_column_first=True)
        except ReadFileException as e:
            app_logger.error(e)
            exit(1)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]
        return counts, meta_raw
