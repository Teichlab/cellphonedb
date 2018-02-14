import os

import pandas as pd
from flask_testing import TestCase

from cellphonedb.api import create_app
from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.flaskcollectorlauncher import FlaskCollectorLauncher


class TestCollectionCalls(TestCase):

    def test_collect_data(self):
        cellphonedb_flask.cellphonedb.database_manager.database.drop_everything()
        cellphonedb_flask.cellphonedb.database_manager.database.create_all()

        self.check_proteins()
        self.check_genes()
        self.check_complex()

    def check_proteins(self):
        self.collect_data('protein')
        self.assert_number_data('protein')

        proteins_expected = pd.read_csv('{}/{}'.format(self.fixtures_dir(), 'collect_protein.csv'))
        multidatas_db = cellphonedb_flask.cellphonedb.database_manager.get_repository('multidata').get_all()

        self.assertEqual(len(proteins_expected), len(multidatas_db),
                         'Database collected multidata (from proteins) didnt match')

    def check_genes(self):
        self.collect_data('gene')
        self.assert_number_data('gene')

    def check_complex(self):
        self.collect_data('complex')
        self.assert_number_data('complex')

    def assert_number_data(self, name):
        namefile = 'collect_{}.csv'.format(name)

        db_data = cellphonedb_flask.cellphonedb.database_manager.get_repository(name).get_all()

        expected_data = pd.read_csv('{}/{}'.format(self.fixtures_dir(), namefile))
        self.assertEqual(len(db_data), len(expected_data), 'Database collected {} didnt match'.format(name))

    def collect_data(self, name):
        namefile = 'collect_{}.csv'.format(name)
        getattr(FlaskCollectorLauncher(), name)(namefile, self.fixtures_dir())

    def create_app(self):
        return create_app(environment='test')

    @staticmethod
    def fixtures_dir():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        fixtures_dir = '{}/fixtures'.format(current_dir)

        return fixtures_dir
