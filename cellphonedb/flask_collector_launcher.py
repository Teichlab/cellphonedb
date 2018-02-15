import pandas as pd

from cellphonedb.api import data_dir
from cellphonedb.extensions import cellphonedb_flask


class FlaskCollectorLauncher(object):
    def __getattr__(self, method_name):

        def wrapper(namefile='', data_path=''):
            if not namefile:
                namefile = '{}.csv'.format(method_name)

            if not data_path:
                data_path = data_dir

            data = pd.read_csv('{}/{}'.format(data_path, namefile))

            getattr(cellphonedb_flask.cellphonedb.collect, method_name)(data)

        return wrapper

    def all(self, protein_filename='', gene_filename='', complex_filename='', interaction_filename='', data_path=''):
        print('Collecting Proteins')
        self.protein(protein_filename, data_path)
        print('Collecting Genes')
        self.gene(gene_filename, data_path)
        print('Collecting Complexes')
        self.complex(complex_filename, data_path)
        print('Collecting Interactions')
        self.interaction(interaction_filename, data_path)
#
