import os
import random
import string
import time

from flask_testing import TestCase

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.local_launchers.local_collector_launcher import LocalCollectorLauncher
from cellphonedb.utils import utils


class CellphoneFlaskTestCase(TestCase):
    @staticmethod
    def fixtures_dir():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        fixtures_dir = '{}/fixtures'.format(current_dir)

        return fixtures_dir

    @staticmethod
    def reset_db():
        cellphonedb_app.cellphonedb.database_manager.database.drop_everything()
        cellphonedb_app.cellphonedb.database_manager.database.create_all()

    def populate_db(self):
        LocalCollectorLauncher().all('collect_protein.csv', 'collect_gene.csv', 'collect_complex.csv',
                                             'collect_interaction.csv', self.fixtures_dir())

    @staticmethod
    def remove_file(file):
        os.remove(file)

    @staticmethod
    def rand_string(digits=5):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(digits))

    @staticmethod
    def get_test_filename(original_namefile, extension, prefix='TESTING'):
        namefile = '{}_{}_{}_{}.{}'.format(prefix, original_namefile, int(time.time()),
                                           CellphoneFlaskTestCase.rand_string(),
                                           extension)

        return namefile

    def assert_file_not_empty(self, file, message=''):
        if not message:
            message = 'File {} is empty'.format(file)

        read_data = utils.read_data_table_from_file(file)
        self.assertFalse(read_data.empty, message)

    def assert_file_exist(self, path_file, message=''):
        if not message:
            message = 'File {} didnt exist'.format(path_file)

        self.assertTrue(os.path.isfile(path_file), message)
