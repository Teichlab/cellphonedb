import json

from cellphonedb.flask_app import create_app, data_test_dir
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestRestApi(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(environment='test', raise_non_defined_vars=False)

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def test_cluster_receptor_ligand_interactions_unprocessed(self):
        parameters = json.dumps({'threshold': 0.2, 'enable_integrin': True, 'enable_complex': True})

        response = self.client.post(
            '/api/cluster_receptor_ligand_interactions_unprocessed',

            content_type='multipart/form-data', data=
            {'parameters': parameters,
             'meta_file': (
                 '{}/{}'.format(data_test_dir, 'query_meta.csv'), 'test_meta.txt', 'text/csv'),
             'counts_file': (
                 '{}/{}'.format(data_test_dir, 'query_counts.csv'), 'test_counts.txt',
                 'text/csv')
             })

        self.assert200(response)

    def test_cluster_receptor_ligand_interactions(self):
        self._assert_cluster_receptor_ligand_interactions_query('query_cells_to_clusters.csv', 'text/csv', 0.2, True,
                                                                True)

    def _assert_cluster_receptor_ligand_interactions_query(self, file_name: str, content_type: str, threshold: float,
                                                           enable_integrin: bool, enable_complex: bool):
        parameters = json.dumps(
            {'threshold': threshold, 'enable_integrin': enable_integrin, 'enable_complex': enable_complex})

        response = self.client.post(
            '/api/cluster_receptor_ligand_interactions',

            content_type='multipart/form-data', data=
            {'parameters': parameters,
             'cell_to_clusters_file': (
                 '{}/{}'.format(data_test_dir, file_name), file_name,
                 content_type),
             })

        self.assert200(response)
