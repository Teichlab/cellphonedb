import os

from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestFlaskQueryCalls(CellphoneFlaskTestCase):

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def create_app(self):
        return create_app('test')

    def test_cell_to_cluster_real_data(self):
        FlaskTerminalQueryLauncher().cells_to_clusters('query_meta.csv', 'query_counts.csv', data_test_dir,
                                                       output_test_dir)

        self.assert_file_exist('cells_to_clusters.csv')

    def assert_file_exist(self, namefile, message=''):
        if not message:
            message = 'File {} didnt exist'.format(namefile)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assertTrue(os.path.isfile(path_file), message)
        self.remove_file(path_file)
