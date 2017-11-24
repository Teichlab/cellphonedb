import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.collection import Collector
from cellcommdb.config import TestConfig
from cellcommdb.extensions import db
from cellcommdb.models import Complex, Protein, Multidata, Interaction, ComplexComposition, Gene


class DatabaseNumberOfEntries(TestCase):
    def test_protein(self):
        query = db.session.query(Protein.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 5153, 'Number of Protein entries are different')

    def test_gene(self):
        query = db.session.query(Gene.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 5821, 'Number of Gene entries are different')

    def test_complex(self):
        query = db.session.query(Complex.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 236, 'Number of Complex entries are different')

    def test_multidata(self):
        query = db.session.query(Multidata.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 5389, 'Number of Multidata entries are different')

    def test_protein_complex(self):
        query = db.session.query(Multidata.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        number_of_multidata = len(dataframe)

        query = db.session.query(Protein.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        number_of_protein = len(dataframe)

        query = db.session.query(Complex.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        number_of_complex = len(dataframe)

        self.assertEqual(number_of_multidata, number_of_complex + number_of_protein,
                         'Number of multidata is diferent than proteins+complex')

    def test_interaction(self):
        query = db.session.query(Interaction.id, Interaction.source)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 9650, 'Number of interactions not equal')

    def test_interaction_curated(self):
        query = db.session.query(Interaction.id, Interaction.source)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe[dataframe['source'] == 'curated']), 95,
                         'Number of curated interactions not equal')

    def test_complex_composition(self):
        query = db.session.query(ComplexComposition.id)
        dataframe = pd.read_sql(query.statement, db.engine)

        self.assertEqual(len(dataframe), 497, 'Number of Complex Composition entries are different')

    def create_app(self):
        return create_app(TestConfig)

    def _populate_db(self):
        with self.app.app_context():
            collector = Collector(self.app)
            collector.all()

    def setUp(self):
        # self._clear_db()
        # db.create_all()
        # self._populate_db()

        self.client = self.app.test_client()

    @staticmethod
    def _clear_db():
        db.session.remove()
        db.reflect()
        db.drop_all()
