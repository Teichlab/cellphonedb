import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.config import TestConfig
from cellcommdb.extensions import db
from cellcommdb.models import Protein, Gene


class DatabaseRelationsChecks(TestCase):
    def test_all_protein_have_gen(self):
        protein_query = db.session.query(Protein.id)
        protein_ids = pd.read_sql(protein_query.statement, db.engine)['id'].tolist()

        gene_query = db.session.query(Gene.protein_id)
        gene_protein_ids = pd.read_sql(gene_query.statement, db.engine)['protein_id'].tolist()

        protein_without_gene = []
        for protein_id in protein_ids:
            if not protein_id in gene_protein_ids:
                protein_without_gene.append(protein_id)

        assert len(protein_without_gene) == 0

    def setUp(self):
        self.client = self.app.test_client()

    def create_app(self):
        return create_app(TestConfig)
