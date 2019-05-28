import pandas as pd

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import cellphonedb_app, data_dir
from cellphonedb.utils import utils


class LocalCollectorLauncher(object):
    def __getattr__(self, method_name):
        def wrapper(namefile='', data_path=''):
            app_logger.info('Collecting {}'.format(method_name))
            if not namefile:
                namefile = '{}_input.csv'.format(method_name)

            if not data_path:
                data_path = data_dir

            data = utils.read_data_table_from_file('{}/{}'.format(data_path, namefile))

            getattr(cellphonedb_app.cellphonedb.collect, method_name)(data)

        return wrapper

    def all(self, protein_filename='', gene_filename='', complex_filename='', interaction_filename='', data_path=''):
        self.protein(protein_filename, data_path)
        self.gene(gene_filename, data_path)
        self.complex(complex_filename, data_path)
        self.interaction(interaction_filename, data_path)
