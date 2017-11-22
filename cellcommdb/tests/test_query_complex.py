import os
import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.config import TestConfig

data_query = 'test'


class QueryComplexChecks(TestCase):
    def test_files(self):
        test_data_dir = './cellcommdb/tests/test_data/%s/r-s/complex/results' % data_query
        generated_data_dir = './out/complexes'
        namefiles_original = os.listdir(test_data_dir)

        namefiles_original = list(filter(lambda name: name.endswith('.txt'), namefiles_original))
        not_equal = False
        for namefile in namefiles_original:
            file_original = open('%s/%s' % (test_data_dir, namefile))
            original_df = pd.read_csv(file_original, sep='\t')
            file_original.close()

            file_generated = open('%s/%s' % (generated_data_dir, namefile))

            generated_df = pd.read_csv(file_generated, '\t')
            file_generated.close()

            self.assertEqual(len(original_df), len(generated_df), 'The length of %s is different' % namefile)

            original_df = original_df.sort_values(['Name_L']).reset_index(drop=True)
            generated_df = generated_df.sort_values(['Name_L']).reset_index(drop=True)
            if not original_df.equals(generated_df):
                print('%s is different' % namefile)

                not_equal = True

        self.assertFalse(not_equal, 'Some query complex output files are different')

    def _check_file(self, namefile, sep=',', order_by=None,
                    test_data_dir='./cellcommdb/tests/test_data/%s/r-s/complex' % data_query,
                    generated_data_dir='./out'):
        file_original = open('%s/%s' % (test_data_dir, namefile))
        file_generated = open('%s/%s' % (generated_data_dir, namefile))

        original_df = pd.read_csv(file_original, sep=sep)
        generated_df = pd.read_csv(file_generated, sep=sep)

        file_original.close()
        file_generated.close()

        if order_by:
            self.assertEqual(len(original_df), len(generated_df), 'Number of %s not equal' % namefile)
        else:
            self.assertEqual(len(original_df), len(generated_df), 'Number of %s not equal' % namefile)

        self.assertTrue(original_df.sort_values(order_by).reset_index(drop=True).equals(
            generated_df.sort_values(order_by).reset_index(drop=True)), 'Content File %s isnt equal' % namefile)

    def test_complex_filtered(self):
        self._check_file('TEST_complex_filtered.txt', '\t', order_by='interaction_id')

    def setUp(self):
        self.client = self.app.test_client()

    def create_app(self):
        return create_app(TestConfig)
