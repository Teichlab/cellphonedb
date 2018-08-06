import pandas as pd

from cellphonedb.app.app_logger import app_logger
from cellphonedb.app.flask.flask_app import data_dir
from cellphonedb.app.flask.flask_extensions import cellphonedb_flask


class FlaskTerminalCollectorLauncher(object):
    def __getattr__(self, method_name):
        def wrapper(namefile='', data_path=''):
            app_logger.info('Collecting {}'.format(method_name))
            if not namefile:
                namefile = '{}.csv'.format(method_name)

            if not data_path:
                data_path = data_dir

            data = pd.read_csv('{}/{}'.format(data_path, namefile))

            getattr(cellphonedb_flask.cellphonedb.collect, method_name)(data)

        return wrapper

    def all(self, protein_filename='', gene_filename='', complex_filename='', interaction_filename='', data_path=''):
        self.protein(protein_filename, data_path)
        self.gene(gene_filename, data_path)
        self.complex(complex_filename, data_path)
        self.interaction(interaction_filename, data_path)
