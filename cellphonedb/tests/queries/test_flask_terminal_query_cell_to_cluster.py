from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestFlaskTerminalQueryCalls(CellphoneFlaskTestCase):

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def create_app(self):
        return create_app(environment='test', raise_non_defined_vars=False)

    def test_cell_to_cluster(self):
        namefile = self.get_test_filename('cells_to_clusters', 'csv')
        FlaskTerminalQueryLauncher().cells_to_clusters('query_meta.csv', 'query_counts.csv', data_test_dir,
                                                       output_test_dir, result_namefile=namefile)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assert_file_exist(path_file)
        self.assert_file_not_empty(path_file)
        self.remove_file(path_file)
