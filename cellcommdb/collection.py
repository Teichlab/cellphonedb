import os
import pandas as pd
import numpy as np

from cellcommdb.api import current_dir
from cellcommdb.collections import protein, complex, unity_interaction, interaction
from cellcommdb.extensions import db
from cellcommdb.models import *
from cellcommdb.api import create_app


class Collector(object):
    def __init__(self, app):
        self.app = app

    def gene(self, gene_file=None):
        if not gene_file:
            gene_file = os.path.join(current_dir, 'data', 'gene_table.csv')

        with self.app.app_context():
            # Query for existing genes

            existing_genes = db.session.query(Gene.ensembl).all()
            existing_genes = [g[0] for g in existing_genes]

            # Query for proteins in order to join
            proteins = db.session.query(Protein.uniprot, Protein.id).all()
            proteins = {p[0]: p[1] for p in proteins}

            gene_df = pd.read_csv(gene_file, quotechar='"')

            # Remove genes already in db
            gene_df = gene_df[gene_df['ensembl'].apply(
                lambda x: x not in existing_genes)]

            gene_df['protein_id'] = gene_df['protein_uniprot'].replace(proteins)
            gene_df['protein_id'] = gene_df['protein_id'].apply(
                lambda x: x if isinstance(x, int) else np.nan)
            gene_df[['ensembl', 'name', 'protein_id']].to_sql(
                name='gene', if_exists='append', con=db.engine, index=False)

    def protein(self, protein_file=None):
        with self.app.app_context():
            protein.load(protein_file)

    def complex(self, complex_file=None):
        with self.app.app_context():
            complex.load(complex_file)

    def unity_interaction(self, unity_interaction_file=None):
        with self.app.app_context():
            unity_interaction.load(unity_interaction_file)

    def interaction(self, interaction_file=None):
        with self.app.app_context():
            interaction.load(interaction_file)


if __name__ == "__main__":
    app = create_app()
    collector = Collector(app)
    collector.complex()
