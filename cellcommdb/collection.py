from cellcommdb.collections import protein, complex, interaction, gene
from cellcommdb.api import create_app


class Collector(object):
    def __init__(self, app):
        self.app = app

    def protein(self, protein_file=None):
        with self.app.app_context():
            protein.load(protein_file)

    def gene(self, gene_file=None):
        with self.app.app_context():
            gene.load(gene_file)

    def complex(self, complex_file=None):
        with self.app.app_context():
            complex.load(complex_file)

    def interaction(self, interaction_file=None):
        with self.app.app_context():
            interaction.load(interaction_file)

    def all(self, filename=None):
        with self.app.app_context():
            print('Collecting Proteins')
            protein.load()
            print('Collecting Genes')
            gene.load()
            print('Collecting Complexes')
            complex.load()
            print('Collecting Interactions')
            interaction.load()


if __name__ == "__main__":
    app = create_app()
    collector = Collector(app)
    collector.complex()
