import random
import string

from flask_testing import TestCase

from cellphonedb.api import create_app, output_test_dir
from cellphonedb.flaskexporterlauncher import FlaskExporterLauncher

import os.path


class TestExportersCalls(TestCase):

    def test_ligands_receptors_proteins(self):
        namefile = 'TESTING_test_exporter_calls_ligands_receptors_proteins_' + self.rand_string() + '.csv'
        FlaskExporterLauncher.ligands_receptors_proteins(namefile, output_test_dir)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assertTrue(os.path.isfile(path_file))
        self.remove_file(path_file)

    def test_complex(self):
        namefile = 'TESTING_test_exporter_complex_' + self.rand_string() + '.csv'
        FlaskExporterLauncher.complex(namefile, output_test_dir)

        path_file = '{}/{}'.format(output_test_dir, namefile)
        self.assertTrue(os.path.isfile(path_file))
        self.remove_file(path_file)

    def remove_file(self, file):
        os.remove(file)

    def rand_string(self, digits=5):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(digits))

    def create_app(self):
        return create_app(environment='test')
