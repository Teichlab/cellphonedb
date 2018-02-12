import random
import string

from flask_testing import TestCase

from cellphonedb.api import create_app, output_test_dir
from cellphonedb.flaskexporterlauncher import FlaskExporterLauncher

import os.path


class TestExportersCalls(TestCase):

    def test_ligands_receptors_proteins(self):
        self.assert_file_exist('exporter_calls_ligands_receptors_proteins', 'csv',
                               FlaskExporterLauncher.ligands_receptors_proteins)

    def test_complex(self):
        self.assert_file_exist('exporter_complex', 'csv', FlaskExporterLauncher.complex)

    def test_complex_web(self):
        self.assert_file_exist('exporter_complex_web', 'csv', FlaskExporterLauncher.complex_web)

    def test_interaction(self):
        self.assert_file_exist('interactions', 'csv', FlaskExporterLauncher.interaction)

    def test_receptor_ligand_interaction(self):
        self.assert_file_exist('receptor_ligand_interaction', 'csv', FlaskExporterLauncher.receptor_ligand_interaction)

    def assert_file_exist(self, expected_name, expected_extension, function_call, message=''):
        namefile = self.get_test_namefile('%s' % expected_name, expected_extension)
        if not message:
            message = 'File {} didnt exist'.format(namefile)

        function_call(namefile, output_test_dir)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assertTrue(os.path.isfile(path_file), message)
        self.remove_file(path_file)

    @staticmethod
    def remove_file(file):
        os.remove(file)

    @staticmethod
    def rand_string(digits=5):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(digits))

    @staticmethod
    def get_test_namefile(original_namefile, extension, prefix='TESTING'):
        namefile = '{}_{}_{}.{}'.format(prefix, original_namefile, TestExportersCalls.rand_string(), extension)

        return namefile

    def create_app(self):
        return create_app(environment='test')
