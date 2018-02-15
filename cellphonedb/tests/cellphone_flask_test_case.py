import os
import random
import string

from flask_testing import TestCase

from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.flask_collector_launcher import FlaskCollectorLauncher


class CellphoneFlaskTestCase(TestCase):
    @staticmethod
    def fixtures_dir():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        fixtures_dir = '{}/fixtures'.format(current_dir)

        return fixtures_dir

    def reset_db(self):
        cellphonedb_flask.cellphonedb.database_manager.database.drop_everything()
        cellphonedb_flask.cellphonedb.database_manager.database.create_all()

    def populate_db(self):
        FlaskCollectorLauncher().all('collect_protein.csv', 'collect_gene.csv', 'collect_complex.csv',
                                     'collect_interaction.csv', self.fixtures_dir())

    @staticmethod
    def remove_file(file):
        os.remove(file)

    @staticmethod
    def rand_string(digits=5):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(digits))

    @staticmethod
    def get_test_namefile(original_namefile, extension, prefix='TESTING'):
        namefile = '{}_{}_{}.{}'.format(prefix, original_namefile, CellphoneFlaskTestCase.rand_string(), extension)

        return namefile
