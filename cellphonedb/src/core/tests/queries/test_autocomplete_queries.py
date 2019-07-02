import random
from unittest import TestCase

from cellphonedb.src.app.app_config import AppConfig
from cellphonedb.src.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy


class TestAutocompleteQueries(TestCase):

    def setUp(self) -> None:
        self.cellphone = CellphonedbSqlalchemy(AppConfig().get_cellphone_core_config())
        gene_repository = self.cellphone.database_manager.get_repository('gene')
        self.all_genes = gene_repository.get_all_expanded().to_dict(orient='records')

    def test_find_elements_by_gene_name(self):
        self._test_find_elements_by_('gene_name')

    def test_find_elements_by_protein_name(self):
        self._test_find_elements_by_('protein_name')

    def test_find_elements_by_hgnc_symbol(self):
        self._test_find_elements_by_('hgnc_symbol')

    def test_find_elements_by_ensembl(self):
        self._test_find_elements_by_('ensembl')

    def test_find_elements_by_name(self):
        self._test_find_elements_by_('name')

    def _test_find_elements_by_(self, field):
        random_gene = random.choice(self.all_genes)
        whole_input = random_gene[field]

        whole_query_result = self.cellphone.query.autocomplete_launcher(whole_input)

        whole_results = whole_query_result['value'].tolist()
        self.assertIn(whole_input, whole_results)

        partial_input = self._random_substring(whole_input)

        partial_query_result = self.cellphone.query.autocomplete_launcher(partial_input)

        partial_results = partial_query_result['value'].tolist()
        self.assertIn(whole_input, partial_results)

        self.assertGreaterEqual(len(partial_results), len(whole_results))

    def _random_substring(self, whole_input):
        start_index = self._random_position_to_half(whole_input)
        end_index = self._random_position_to_half(whole_input)

        return whole_input[start_index:-end_index if end_index else None]

    @staticmethod
    def _random_position_to_half(string):
        return random.randint(0, int((len(string)) / 2))
