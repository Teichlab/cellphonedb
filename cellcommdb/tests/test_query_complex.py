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
        namefiles_generated = os.listdir(generated_data_dir)

        namefiles_original = list(filter(lambda name: name.endswith('.txt'), namefiles_original))
        namefiles_generated = list(filter(lambda name: name.endswith('.txt'), namefiles_generated))

        for namefile in namefiles_original:
            namefile = 'Cluster_Endothelial_Cluster_Cycling_NK_min0.txt'
            file_original = open('%s/%s' % (test_data_dir, namefile))
            original_df = pd.read_csv(file_original, sep='\t')
            file_original.close()

            file_generated = open('%s/%s' % (generated_data_dir, namefile))

            generated_df = pd.read_csv(file_generated, '\t')
            file_generated.close()

            self.assertEqual(len(original_df), len(generated_df), 'The length of %s is different' % namefile)

            columns = ['Unity_L', 'Name_L', 'Gene_L', 'Gene_L_ens', 'Receptor_L', 'Membrane_L', 'Secretion_L',
                       'Ligand_L', 'Adhesion_L', 'Unity_R', 'Name_R', 'Gene_R', 'Gene_R_ens', 'Receptor_R',
                       'Membrane_R', 'Secretion_R', 'Ligand_R', 'Adhesion_R', 'Total_cells_L',
                       'Num_cells_L', 'Sum_Up_L', 'Total_cells_R', 'Num_cells_R', 'Sum_Up_R',
                       'Mean_Sum']

            original_df = original_df[columns].sort_values(['Name_L']).reset_index(drop=True)
            generated_df = generated_df[columns].sort_values(['Name_L']).reset_index(drop=True)
            if not original_df.equals(generated_df):
                print('%s is different' % namefile)

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
