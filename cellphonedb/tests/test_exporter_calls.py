from cellphonedb.flask_app import create_app, output_test_dir
from cellphonedb.flask_terminal_exporter_launcher import FlaskTerminalExporterLauncher

import os.path

from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestExporterCalls(CellphoneFlaskTestCase):

    def test_complex(self):
        self.assert_file_exist('complex')

    def test_complex_web(self):
        self.assert_file_exist('complex_web')

    def test_interaction(self):
        self.assert_file_exist('interaction')

    def test_protein(self):
        self.assert_file_exist('protein')

    def test_gene(self):
        self.assert_file_exist('gene')

    def assert_file_exist(self, method_name, message='', expected_extension='csv', expected_namefile=''):
        if not expected_namefile:
            expected_namefile = '{}'.format(method_name)

        namefile = self.get_test_namefile(expected_namefile, expected_extension)
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
        return create_app(environment='test')
