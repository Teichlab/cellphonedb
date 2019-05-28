import os
from typing import Optional

import pandas as pd

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import output_dir
from cellphonedb.src.core.utils.subsampler import Subsampler
from cellphonedb.utils import utils
from cellphonedb.utils.utils import _get_separator


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
                                                        iterations: int = 1000,
                                                        threshold: float = 0.1,
                                                        output_path: str = '',
                                                        output_format: Optional[str] = None,
                                                        means_filename: str = 'means',
                                                        pvalues_filename: str = 'pvalues',
                                                        significant_means_filename: str = 'significant_means',
                                                        deconvoluted_filename='deconvoluted',
                                                        debug_seed: int = -1,
                                                        threads: int = -1,
                                                        result_precision: int = 3,
                                                        pvalue: float = 0.05,
                                                        subsampler: Subsampler = None,
                                                        ) -> None:
        output_path = self._set_paths(output_path, project_name)

        debug_seed = int(debug_seed)
        iterations = int(iterations)
        threads = int(threads)
        threshold = float(threshold)
        result_precision = int(result_precision)

        counts, meta = self._load_meta_counts(counts_filename, meta_filename)

        pvalues_simple, means_simple, significant_means_simple, deconvoluted_simple = \
            self.cellphonedb_app.method.cpdb_statistical_analysis_launcher(
                meta,
                counts,
                iterations,
                threshold,
                threads,
                debug_seed,
                result_precision,
                pvalue,
                subsampler
            )

        self.write_to_file(means_simple, means_filename, output_format, output_path)
        self.write_to_file(pvalues_simple, pvalues_filename, output_format, output_path)
        self.write_to_file(significant_means_simple, significant_means_filename, output_format, output_path)
        self.write_to_file(deconvoluted_simple, deconvoluted_filename, output_format, output_path)

    def cpdb_analysis_local_method_launcher(self, meta_filename: str,
                                            counts_filename: str,
                                            project_name: str = '',
                                            threshold: float = 0.1,
                                            output_path: str = '',
                                            output_format: Optional[str] = None,
                                            means_filename: str = 'means',
                                            significant_means_filename: str = 'significant_means',
                                            deconvoluted_filename='deconvoluted',
                                            result_precision: int = 3,
                                            subsampler: Subsampler = None,
                                            ) -> None:
        output_path = self._set_paths(output_path, project_name)

        result_precision = int(result_precision)
        threshold = float(threshold)

        counts, meta = self._load_meta_counts(counts_filename, meta_filename)

        means, significant_means, deconvoluted = \
            self.cellphonedb_app.method.cpdb_method_analysis_launcher(meta,
                                                                      counts,
                                                                      threshold,
                                                                      result_precision,
                                                                      subsampler)

        self.write_to_file(means, means_filename, output_format, output_path)
        self.write_to_file(significant_means, significant_means_filename, output_format, output_path)
        self.write_to_file(deconvoluted, deconvoluted_filename, output_format, output_path)

    @staticmethod
    def write_to_file(df: pd.DataFrame, filename: str, output_format: Optional[str], output_path: str):
        _, file_extension = os.path.splitext(filename)

        if output_format is None:
            if not file_extension:
                default_format = 'txt'
                default_extension = '.{}'.format(default_format)

                separator = _get_separator(default_extension)
                filename = '{}{}'.format(filename, default_extension)
            else:
                separator = _get_separator(file_extension)
        else:
            selected_extension = '.{}'.format(output_format)

            if file_extension != selected_extension:
                separator = _get_separator(selected_extension)
                filename = '{}{}'.format(filename, selected_extension)

                if file_extension:
                    app_logger.warning(
                        'Selected extension missmatches output filename ({}, {}): It will be added => {}'.format(
                            selected_extension, file_extension, filename))
            else:
                separator = _get_separator(selected_extension)

        df.to_csv('{}/{}'.format(output_path, filename), sep=separator, index=False)

    @staticmethod
    def _path_is_empty(path):
        return bool([f for f in os.listdir(path) if not f.startswith('.')])

    @staticmethod
    def _set_paths(output_path, project_name):
        if not output_path:
            output_path = output_dir
        if project_name:
            output_path = os.path.realpath(os.path.expanduser('{}/{}'.format(output_path, project_name)))
        os.makedirs(output_path, exist_ok=True)
        if LocalMethodLauncher._path_is_empty(output_path):
            app_logger.warning(
                'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))
        return output_path

    @staticmethod
    def _load_meta_counts(counts_filename: str, meta_filename: str) -> (pd.DataFrame, pd.DataFrame):
        """
        :raise ParseMetaException
        """
        meta = utils.read_data_table_from_file(os.path.realpath(meta_filename))
        counts = utils.read_data_table_from_file(os.path.realpath(counts_filename), index_column_first=True)

        return counts, meta
