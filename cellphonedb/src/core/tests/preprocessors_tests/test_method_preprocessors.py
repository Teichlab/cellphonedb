import pandas as pd
from unittest import TestCase

from cellphonedb.src.core.Cellphonedb import data_test_dir
from cellphonedb.src.core.exceptions.ProcessMetaException import ProcessMetaException
from cellphonedb.src.core.preprocessors import method_preprocessors


class TestMethodPreprocessorsTest(TestCase):

    def test_two_column_both_defined(self):
        self._meta_file_validator('meta_two_columns_both_defined.txt')

    def test_multiple_columns_all_defined(self):
        self._meta_file_validator('meta_multiple_columns_all_defined.txt')

    def test_two_columns_none_defined(self):
        self._meta_file_validator('meta_two_columns_none_defined.txt')

    def test_multiple_columns_only_celltype_defined(self):
        self._meta_file_validator('meta_multiple_columns_celltype_defined.txt')

    def test_incomplete_header(self):
        self._meta_file_validator('meta_multiple_columns_miss_one_header.txt')

    def test_multiple_column_insensitive_case(self):
        self._meta_file_validator('meta_multiple_columns_random_uppercase.txt')

    def test_one_column_fail(self):
        self._meta_file_exception_validator('meta_one_column_fail.txt')

    def test_wrong_format_fail(self):
        self._meta_file_exception_validator('meta_wrong_format_fail.txt')

    def test_multiple_column_miss_multiple_header(self):
        self._meta_file_exception_validator('meta_multiple_columns_miss_multiple_header_fail.txt')

    def _meta_file_exception_validator(self, raw_meta_file):
        raw_meta = pd.read_csv('{}/preprocessors_fixtures/{}'.format(data_test_dir, raw_meta_file), sep='\t')
        with self.assertRaises(ProcessMetaException):
            method_preprocessors.meta_preprocessor(raw_meta)

    def _meta_file_validator(self, raw_meta_file: str) -> None:
        raw_meta = pd.read_csv('{}/preprocessors_fixtures/{}'.format(data_test_dir, raw_meta_file), sep='\t')
        meta = method_preprocessors.meta_preprocessor(raw_meta)

        result_expected = pd.read_csv(
            '{}/preprocessors_fixtures/meta_result_preprocessor.txt'.format(data_test_dir),
            sep='\t', index_col=0)

        self.assertTrue(meta.equals(result_expected))
        self.assertEqual(meta.index.name, 'cell')
