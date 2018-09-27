import pandas as pd

from src.app.app_logger import app_logger
from src.app.cellphonedb_app import cellphonedb_app, data_dir


class LocalCollectorLauncher(object):
    def __getattr__(self, method_name):
        def wrapper(namefile='', data_path=''):
            app_logger.info('Collecting {}'.format(method_name))
            if not namefile:
                namefile = '{}.csv'.format(method_name)

            if not data_path:
                data_path = data_dir

            data = pd.read_csv('{}/{}'.format(data_path, namefile))

            getattr(cellphonedb_app.cellphonedb.collect, method_name)(data)

        return wrapper

    def all(self, protein_filename='', gene_filename='', complex_filename='', interaction_filename='', data_path=''):
        self.protein(protein_filename, data_path)
        self.gene(gene_filename, data_path)
        self.complex(complex_filename, data_path)
        self.interaction(interaction_filename, data_path)
