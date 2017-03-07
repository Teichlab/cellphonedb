import os
import pandas as pd
import numpy as np

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import *
from cellcommdb.api import create_app


def collect_genes(app, gene_file=None):

    if not gene_file:
        gene_file = os.path.join(current_dir, 'data', 'gene_table.csv')

    with app.app_context():

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


def collect_proteins(app, protein_file=None):

    with app.app_context():
        if not protein_file:
            protein_file = os.path.join(current_dir, 'data', 'protein.csv')

        prot_df = pd.read_csv(protein_file)
        existing_proteins = db.session.query(Protein.uniprot).all()
        existing_proteins = [p[0] for p in existing_proteins]

        prot_df = prot_df[prot_df['uniprot'].apply(
            lambda x: x not in existing_proteins)]
        prot_df.drop_duplicates(subset=['uniprot'], inplace=True)
        prot_df = prot_df.iloc[:, 1:]
        prot_df.drop('gene_name', axis=1, inplace=True)

        # Convert to boolean
        bools = ['transmembrane', 'secretion', 'peripheral', 'receptor',
                 'receptor_highlight', 'adhesion', 'other', 'transporter',
                 'secreted_highlight']
        prot_df[bools] = prot_df[bools].astype(bool)
        prot_df.to_sql(name='protein', if_exists='append', con=db.engine,
                       index=False)


if __name__ == "__main__":
    app = create_app()
    # collect_proteins(app)
    collect_genes(app)
