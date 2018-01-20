import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.extensions import db
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


class DatabaseRelationsChecks(TestCase):
    def test_all_protein_have_gen(self):

        expected_protein_without_gene = 226
        protein_query = db.session.query(Protein, Multidata.name).join(Multidata)

        protein_df = pd.read_sql(protein_query.statement, db.engine)
        protein_ids = protein_df['id_protein'].tolist()

        gene_query = db.session.query(Gene.protein_id)
        gene_protein_ids = pd.read_sql(gene_query.statement, db.engine)['protein_id'].tolist()

        protein_without_gene = []
        for protein_id in protein_ids:
            if not protein_id in gene_protein_ids:
                protein_without_gene.append(protein_df[protein_df['id_protein'] == protein_id]['name'].iloc[0])

        if len(protein_without_gene) > expected_protein_without_gene:
            print('There are %s Proteins without gene' % len(protein_without_gene))
            print(protein_without_gene)

        self.assertEqual(len(protein_without_gene), expected_protein_without_gene, 'There are Proteins without Gene.')

    def setUp(self):
        self.client = self.app.test_client()

    def create_app(self):
        return create_app(environment='test')
