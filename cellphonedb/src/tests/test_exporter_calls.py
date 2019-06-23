from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.app.cellphonedb_app import output_test_dir
from cellphonedb.src.local_launchers.local_exporter_launcher import LocalExporterLauncher

import os

from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestExporterCalls(CellphoneFlaskTestCase):

    def test_all_exporter_generators(self):
        exporters = ['complex', 'interaction', 'protein', 'gene', 'protein_complex_cellphonedb']

        for exporter in exporters:
            self.assert_file_exist(exporter)

    def assert_file_exist(self, method_name, message='', expected_extension='csv', expected_namefile=''):
        if not expected_namefile:
            expected_namefile = '{}'.format(method_name)

        namefile = self.get_test_filename(expected_namefile, expected_extension)
        if not message:
            message = 'File {} didnt exist'.format(namefile)

        getattr(LocalExporterLauncher(), method_name)(namefile, output_test_dir)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assertTrue(os.path.isfile(path_file), message)
        self.remove_file(path_file)

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def create_app(self):
        return create_app(environment='test', raise_non_defined_vars=False)
