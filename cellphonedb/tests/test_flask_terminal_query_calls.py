import os

from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase
from utils import utils


class TestFlaskTerminalQueryCalls(CellphoneFlaskTestCase):

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def create_app(self):
        return create_app('test')

    def test_cell_to_cluster(self):
        FlaskTerminalQueryLauncher().cells_to_clusters('query_meta.csv', 'query_counts.csv', data_test_dir,
                                                       output_test_dir)

        namefile = 'cells_to_clusters.csv'
        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assert_file_exist(path_file)
        self.assert_file_not_empty(path_file)
        self.remove_file(path_file)

    def assert_file_not_empty(self, file, message=''):
        if not message:
            message = 'File {} is empty'.format(file)

        read_data = utils.read_data_table_from_file(file)
        self.assertFalse(read_data.empty, message)

    def assert_file_exist(self, path_file, message=''):
        if not message:
            message = 'File {} didnt exist'.format(path_file)

        self.assertTrue(os.path.isfile(path_file), message)
