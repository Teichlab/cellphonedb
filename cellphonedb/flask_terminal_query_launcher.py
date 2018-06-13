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

    def cells_to_clusters(self, meta_namefile, counts_namefile, data_path='', output_path='',
                          result_namefile='cells_to_clusters.csv'):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        result = cellphonedb_flask.cellphonedb.query.cells_to_clusters(meta, counts)

        result.to_csv('{}/{}'.format(output_path, result_namefile))

    def cluster_rl_permutations(self, meta_namefile: str, counts_namefile: str, iterations: str, data_path='',
                                output_path: str = '', means_namefile: str = 'means.txt',
                                pvalues_namefile: str = 'pvalues.txt',
                                pvalues_means_namefile: str = 'pvalues_means.txt',
                                debug_seed: str = '0'):

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        debug_seed = int(debug_seed)
        iterations = int(iterations)

        meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]

        pvalues, means, pvalues_means = cellphonedb_flask.cellphonedb.query.cluster_rl_permutations(
            meta, counts, iterations, debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_namefile), sep='\t', index=False)
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_namefile), sep='\t', index=False)
        pvalues_means.to_csv('{}/{}'.format(output_path, pvalues_means_namefile), sep='\t',
                             index=False)

    def cluster_rl_permutations_complex(self, meta_namefile: str, counts_namefile: str, iterations: str, data_path='',
                                        output_path: str = '', means_namefile: str = 'means.txt',
                                        pvalues_namefile: str = 'pvalues.txt', debug_seed: str = '0'):

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        debug_seed = bool(debug_seed)
        iterations = int(iterations)

        meta_raw = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        meta = pd.DataFrame(index=meta_raw.index)
        meta['cell_type'] = meta_raw.iloc[:, 0]

        means, pvalues = cellphonedb_flask.cellphonedb.query.cluster_rl_permutations_complex(meta, counts, iterations,
                                                                                             debug_seed)

        means.to_csv('{}/{}'.format(output_path, means_namefile), sep='\t')
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_namefile), sep='\t')

        # TODO: Add asserts
