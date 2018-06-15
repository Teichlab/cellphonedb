from cellphonedb.flask_app import create_app, output_test_dir
from cellphonedb.flask_terminal_exporter_launcher import FlaskTerminalExporterLauncher

import os

from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestExporterCalls(CellphoneFlaskTestCase):

    def test_all_exporter_generators(self):
        exporters = ['complex', 'complex_web', 'interaction', 'protein', 'gene', 's4_multidata', 's5_heterodimer']

        for exporter in exporters:
            self.assert_file_exist(exporter)

    def assert_file_exist(self, method_name, message='', expected_extension='csv', expected_namefile=''):
        if not expected_namefile:
            expected_namefile = '{}'.format(method_name)

        namefile = self.get_test_filename(expected_namefile, expected_extension)
        if not message:
            message = 'File {} didnt exist'.format(namefile)

        getattr(FlaskTerminalExporterLauncher(), method_name)(namefile, output_test_dir)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assertTrue(os.path.isfile(path_file), message)
        self.remove_file(path_file)

    def setUp(self):
        self.reset_db()
        self.populate_db()

    def create_app(self):
        return create_app(environment='test', raise_non_defined_vars=False)
