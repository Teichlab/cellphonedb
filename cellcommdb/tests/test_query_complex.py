import os
import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.config import TestConfig


class QueryComplexChecks(TestCase):
    def test_files(self):
        test_data_dir = './cellcommdb/tests/test_data/r-s/complex/results'
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

        self.assertFalse(not_equal, 'Some output files are different')

    def test_complex_r_s_filter(self):
        test_data_dir = './cellcommdb/tests/test_data/r-s/complex'
        generated_data_dir = './out/'

        namefile = 'complex_filtered.txt'

        file_original = open('%s/%s' % (test_data_dir, namefile))
        file_generated = open('%s/%s' % (generated_data_dir, namefile))

        original_df = pd.read_csv(file_original, sep='\t')
        generated_df = pd.read_csv(file_generated, sep='\t')

        file_original.close()
        file_generated.close()

        self.assertEqual(len(original_df), len(generated_df), 'Number of Complex Filtered not equal')

        self.assertTrue(original_df.equals(generated_df))

    def setUp(self):
        self.client = self.app.test_client()

    def create_app(self):
        return create_app(TestConfig)
