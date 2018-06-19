import pandas as pd

from cellphonedb.app_logger import app_logger
from cellphonedb.flask_app import output_dir, query_input_dir
from cellphonedb.extensions import cellphonedb_flask
from utils import utils


class FlaskTerminalQueryLauncher(object):
    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            app_logger.info('Launching Query {}'.format(name))

        return method

    @staticmethod
    def cells_to_clusters(meta_filename, counts_filename, data_path='', output_path='',
                          result_filename='cells_to_clusters.csv'):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_filename), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_filename), index_column_first=True)

        result = cellphonedb_flask.cellphonedb.query.cells_to_clusters(meta, counts)

        result.to_csv('{}/{}'.format(output_path, result_filename))

    @staticmethod
    def cluster_statistical_analysis(meta_filename: str, counts_filename: str, iterations: str, data_path='',
                                     output_path: str = '', means_filename: str = 'means.txt',
                                     pvalues_filename: str = 'pvalues.txt',
                                     significant_mean_filename: str = 'significant_means.txt',
                                     means_pvalues_filename: str = 'pvalues_means.txt',
                                     deconvoluted_filename='deconvoluted.txt',
                                     debug_seed: str = '0'):
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

        pvalues_simple, means_simple, significant_means_simple, means_pvalues_simple, deconvoluted_simple = cellphonedb_flask.cellphonedb.query.cluster_statistical_analysis(
            meta, counts, iterations, debug_seed)

        means_simple.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues_simple.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means_simple.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues_simple.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted_simple.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    @staticmethod
    def cluster_statistical_analysis_simple(meta_filename: str, counts_filename: str, iterations: str = '1000',
                                            data_path='', output_path: str = '', means_filename: str = 'means.txt',
                                            pvalues_filename: str = 'pvalues.txt',
                                            significant_mean_filename: str = 'significant_means.txt',
                                            means_pvalues_filename: str = 'pvalues_means.txt',
                                            deconvoluted_filename='deconvoluted.txt',
                                            debug_seed: str = '0'):

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

        pvalues, means, significant_means, means_pvalues, deconvoluted = cellphonedb_flask.cellphonedb.query.cluster_statistical_analysis_simple(
            meta, counts, iterations, debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

    @staticmethod
    def cluster_statistical_analysis_complex(meta_filename: str, counts_filename: str, iterations: str, data_path='',
                                             output_path: str = '', means_filename: str = 'means.txt',
                                             pvalues_filename: str = 'pvalues.txt',
                                             significant_mean_filename: str = 'significant_means.txt',
                                             means_pvalues_filename: str = 'pvalues_means.txt',
                                             deconvoluted_filename='deconvoluted.txt',
                                             debug_seed: str = '0'):

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

        pvalues, means, significant_means, means_pvalues, deconvoluted = cellphonedb_flask.cellphonedb.query.cluster_statistical_analysis_complex(
            meta, counts, iterations, debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_filename), sep='\t', index=False)
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_filename), sep='\t', index=False)
        significant_means.to_csv('{}/{}'.format(output_path, significant_mean_filename), sep='\t', index=False)
        means_pvalues.to_csv('{}/{}'.format(output_path, means_pvalues_filename), sep='\t', index=False)
        deconvoluted.to_csv('{}/{}'.format(output_path, deconvoluted_filename), sep='\t', index=False)

        # TODO: Add asserts
