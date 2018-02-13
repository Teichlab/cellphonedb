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

    # def interaction(self, interaction_file=None):
    #         interaction_collection.load(interaction_file)
    #
    # def all(self, filename=None):
    #         print('Collecting Proteins')
    #         protein_collection.load()
    #         print('Collecting Genes')
    #         gene_collection.load()
    #         print('Collecting Complexes')
    #         complex_collection.load()
    #         print('Collecting Interactions')
    #         interaction_collection.load()
