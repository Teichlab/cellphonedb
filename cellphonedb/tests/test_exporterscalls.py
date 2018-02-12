import random
import string

from flask_testing import TestCase

from cellphonedb.api import create_app, output_test_dir
from cellphonedb.flaskexporterlauncher import FlaskExporterLauncher

import os.path


class TestExportersCalls(TestCase):

    def test_ligands_receptors_proteins(self):
        self.assert_file_exist('ligands_receptors_proteins')

    def test_complex(self):
        self.assert_file_exist('complex')

    def test_complex_web(self):
        self.assert_file_exist('complex_web')

    def test_interaction(self):
        self.assert_file_exist('interaction')

    def test_receptor_ligand_interaction(self):
        self.assert_file_exist('receptor_ligand_interaction')

    def test_protein(self):
        self.assert_file_exist('protein')

    def assert_file_exist(self, method_name, message='', expected_extension='csv', expected_namefile=''):
        if not expected_namefile:
            expected_namefile = '{}'.format(method_name)

        namefile = self.get_test_namefile(expected_namefile, expected_extension)
        if not message:
            message = 'File {} didnt exist'.format(namefile)

        getattr(FlaskExporterLauncher(), method_name)(namefile, output_test_dir)

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
