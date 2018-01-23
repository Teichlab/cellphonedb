import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.collection import Collector
from cellphonedb.extensions import db
from cellphonedb.models.complex.db_model_complex import Complex
from cellphonedb.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.interaction.db_model_interaction import Interaction
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


class DatabaseNumberOfEntries(TestCase):
    def test_protein(self):
        query = db.session.query(Protein.id_protein)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 5269, 'Number of Protein entries are different')

    def test_gene(self):
        query = db.session.query(Gene.id_gene)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 9852, 'Number of Gene entries are different')

    def test_complex(self):
        query = db.session.query(Complex.id_complex)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 240, 'Number of Complex entries are different')

    def test_multidata(self):
        query = db.session.query(Multidata.id_multidata)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 5509, 'Number of Multidata entries are different')

    def test_protein_complex(self):
        query = db.session.query(Multidata.id_multidata)
        dataframe = pd.read_sql(query.statement, db.engine)

        number_of_multidata = len(dataframe)

        query = db.session.query(Protein.id_protein)
        dataframe = pd.read_sql(query.statement, db.engine)

        number_of_protein = len(dataframe)

        query = db.session.query(Complex.id_complex)
        dataframe = pd.read_sql(query.statement, db.engine)

        number_of_complex = len(dataframe)

        self.assertEqual(number_of_multidata, number_of_complex + number_of_protein,
                         'Number of multidata is diferent than proteins+complex')

    def test_interaction(self):
        query = db.session.query(Interaction.id_interaction, Interaction.source)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 10098, 'Number of interactions not equal')

    def test_interaction_curated(self):
        query = db.session.query(Interaction.id_interaction, Interaction.source)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe[dataframe['source'] == 'curated']), 370,
                         'Number of curated interactions not equal')

    def test_complex_composition(self):
        query = db.session.query(ComplexComposition.id_complex_composition)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 506, 'Number of Complex Composition entries are different')

    def create_app(self):
        return create_app(environment='test')

    def _populate_db(self):
        with self.app.app_context():
            collector = Collector(self.app)
            collector.all()

    def setUp(self):
        self.client = self.app.test_client()

    @staticmethod
    def _clear_db():
        db.session.remove()
        db.reflect()
        db.drop_all()
