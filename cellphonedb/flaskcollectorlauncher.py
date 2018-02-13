import pandas as pd

from cellphonedb.api import data_dir
from cellphonedb.extensions import cellphonedb_flask


class FlaskCollectorLauncher(object):
    def protein(self, protein_file='', data_path=''):
        if not protein_file:
            protein_file = 'protein.csv'

        if not data_path:
            data_path = data_dir

        proteins = pd.read_csv('{}/{}'.format(data_path, protein_file))
        cellphonedb_flask.cellphonedb.collect.protein(proteins)

    # def gene(self, gene_file=None):
    #         gene_collection.load(gene_file)
    #
    # def complex(self, complex_file=None):
    #         complex_collection.load(complex_file)
    #
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
