from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestFlaskTerminalQueryCalls(CellphoneFlaskTestCase):

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def create_app(self):
        return create_app('test')

    def test_cell_to_cluster(self):
        namefile = self.get_test_namefile('cells_to_clusters', 'csv')
        FlaskTerminalQueryLauncher().cells_to_clusters('query_meta.csv', 'query_counts.csv', data_test_dir,
                                                       output_test_dir, result_namefile=namefile)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assert_file_exist(path_file)
        self.assert_file_not_empty(path_file)
        self.remove_file(path_file)

    def test_cluster_receptor_ligand_query(self):
        result_namefile = self.get_test_namefile('result', 'csv')
        result_namefile_extended = self.get_test_namefile('resut_extended', 'csv')

        FlaskTerminalQueryLauncher().cluster_receptor_ligand_interactions(
            'query_cells_to_clusters.csv', threshold=0.2, enable_integrin=True, enable_complex=True,
            data_path=data_test_dir, output_path=output_test_dir, result_namefile=result_namefile,
            result_extended_namefile=result_namefile_extended)

        path_result_file = '{}/{}'.format(output_test_dir, result_namefile)
        self.assert_file_exist(path_result_file)
        self.assert_file_not_empty(path_result_file)
        self.remove_file(path_result_file)

        path_result_extended_file = '{}/{}'.format(output_test_dir, result_namefile_extended)
        self.assert_file_exist(path_result_extended_file)
        self.assert_file_not_empty(path_result_extended_file)
        self.remove_file(path_result_extended_file)

    def test_cluster_receptor_ligand_unprocessed_query(self):
        result_cell_to_clusters_namefile = self.get_test_namefile('cell_to_cluster', 'csv')
        result_interaction_namefile = self.get_test_namefile('interaction', 'csv')
        result_interaction_extended_namefile = self.get_test_namefile('interaction_extended', 'csv')

        FlaskTerminalQueryLauncher().cluster_receptor_ligand_interactions_unprocessed(
            'query_meta.csv', 'query_counts.csv', threshold=0.2, enable_integrin=True, enable_complex=True,
            data_path=data_test_dir, output_path=output_test_dir,
            result_cell_to_clusters_namefile=result_cell_to_clusters_namefile,
            result_interaction_namefile=result_interaction_namefile,
            result_interaction_extended_namefile=result_interaction_extended_namefile)

        path_result_file = '{}/{}'.format(output_test_dir, result_cell_to_clusters_namefile)
        self.assert_file_exist(path_result_file)
        self.assert_file_not_empty(path_result_file)
        self.remove_file(path_result_file)

        path_result_interactions = '{}/{}'.format(output_test_dir, result_interaction_namefile)
        self.assert_file_exist(path_result_interactions)
        self.assert_file_not_empty(path_result_interactions)
        self.remove_file(path_result_interactions)

        path_result_extended_file = '{}/{}'.format(output_test_dir, result_interaction_extended_namefile)
        self.assert_file_exist(path_result_extended_file)
        self.assert_file_not_empty(path_result_extended_file)
        self.remove_file(path_result_extended_file)
