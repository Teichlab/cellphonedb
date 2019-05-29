from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import data_dir
from cellphonedb.src.app.cpdb_app import create_app
from cellphonedb.utils import utils


class LocalCollectorLauncher(object):
    app = create_app()

    def __getattr__(self, method_name):
        def wrapper(namefile='', data_path=''):
            app_logger.info('Collecting {}'.format(method_name))
            if not namefile:
                namefile = '{}_input.csv'.format(method_name)

            if not data_path:
                data_path = data_dir

            data = utils.read_data_table_from_file('{}/{}'.format(data_path, namefile))

            getattr(self.app.collect, method_name)(data)

        return wrapper

    def all(self, protein_filename='', gene_filename='', complex_filename='', interaction_filename='', data_path=''):
        self.protein(protein_filename, data_path)
        self.gene(gene_filename, data_path)
        self.complex(complex_filename, data_path)
        self.interaction(interaction_filename, data_path)
