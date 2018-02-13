import os

import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.flaskcollectorlauncher import FlaskCollectorLauncher


class TestCollectionCalls(TestCase):

    def test_collect_protein(self):
        cellphonedb_flask.cellphonedb.database_manager.database.drop_everything()
        cellphonedb_flask.cellphonedb.database_manager.database.create_all()
        protein_namefile = 'collect_protein.csv'
        FlaskCollectorLauncher().protein(protein_namefile, self.fixtures_dir())

        proteins_expected = pd.read_csv('{}/{}'.format(self.fixtures_dir(), protein_namefile))

        proteins_db = cellphonedb_flask.cellphonedb.database_manager.get_repository('protein').get_all()
        multidatas_db = cellphonedb_flask.cellphonedb.database_manager.get_repository('multidata').get_all()

        self.assertEqual(len(proteins_expected), len(proteins_db))
        self.assertEqual(len(proteins_expected), len(multidatas_db))

    def create_app(self):
        return create_app(environment='test')

    @staticmethod
    def fixtures_dir():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        fixtures_dir = '{}/fixtures'.format(current_dir)

        return fixtures_dir
