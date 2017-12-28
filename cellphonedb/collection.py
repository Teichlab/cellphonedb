from cellphonedb.collections import protein_collection, complex_collection, interaction_collection, gene_collection


class Collector(object):
    def __init__(self, app):
        self.app = app

    def protein(self, protein_file=None):
        with self.app.app_context():
            protein_collection.load(protein_file)

    def gene(self, gene_file=None):
        with self.app.app_context():
            gene_collection.load(gene_file)

    def complex(self, complex_file=None):
        with self.app.app_context():
            complex_collection.load(complex_file)

    def interaction(self, interaction_file=None):
        with self.app.app_context():
            interaction_collection.load(interaction_file)

    def all(self, filename=None):
        with self.app.app_context():
            print('Collecting Proteins')
            protein_collection.load()
            print('Collecting Genes')
            gene_collection.load()
            print('Collecting Complexes')
            complex_collection.load()
            print('Collecting Interactions')
            interaction_collection.load()
