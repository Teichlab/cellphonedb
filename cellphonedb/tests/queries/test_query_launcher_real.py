from cellphonedb.app import import_config
from cellphonedb.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy
from cellphonedb.flask_app import output_test_dir, data_test_dir, create_app
from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestQueryLauncherReal(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    def setUp(self):
        super().setUp()
        config = import_config.AppConfig(raise_non_defined_vars=False)
        cellphone_config = config.get_cellphone_core_config()

        self.cellphonedb = CellphonedbSqlalchemy(cellphone_config)

    def test_cell_to_cluster_real_data(self):
        result_namefile = self.get_test_filename('cells_to_clusters', 'csv')
        FlaskTerminalQueryLauncher().cells_to_clusters('real_meta.csv', 'real_counts.csv', data_test_dir,
                                                       output_test_dir, result_namefile)

        path_file = '{}/{}'.format(output_test_dir, result_namefile)
        self.assert_file_exist(path_file)
        self.assert_file_not_empty(path_file)
        self.remove_file(path_file)
