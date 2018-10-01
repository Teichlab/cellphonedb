from unittest import TestCase

import os

import pandas as pd

from cellphonedb.utils import utils


class TestOpenDataFile(TestCase):

    def test_extensions(self):
        extensions = ['csv', 'tsv', 'txt']
        base_name = 'example_data'
        for extension in extensions:
            self.assert_open_file(base_name, extension, False, '')

    def test_custom(self):
        self.assert_open_file('example_data_custom', 'csv', False, ';')

    def assert_open_file(self, base_name, extension, index_column_first, separator):
        fixtures_dir = '{}/fixtures'.format(self.current_dir)
        result = utils.read_data_table_from_file('{}/{}.{}'.format(fixtures_dir, base_name, extension),
                                                 index_column_first, separator)
        expected_result = pd.read_csv('{}/example_data.csv'.format(fixtures_dir))

        self.assertTrue(result.equals(expected_result))

    @property
    def current_dir(self):
        return os.path.dirname(os.path.realpath(__file__))
