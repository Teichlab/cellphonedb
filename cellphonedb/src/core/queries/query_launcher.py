import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.database import DatabaseManager
from cellphonedb.src.core.queries.autocomplete_queries import autocomplete_query
from cellphonedb.src.core.queries.complex import complex_deconvoluted
from cellphonedb.src.core.queries.interaction import interactions_by_element


class QueryLauncher:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def __getattribute__(self, name: str):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Launching Query {}'.format(name))

        return method

    def autocomplete_launcher(self, partial_element) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_all()
        genes = self.database_manager.get_repository('gene').get_all_expanded()[
            ['name', 'ensembl', 'protein_name', 'gene_name', 'hgnc_symbol']]

        return autocomplete_query(genes, multidatas, partial_element)

    def find_interactions_by_element(self, element: str) -> pd.DataFrame:
        interactions = self.database_manager.get_repository('interaction').get_all_expanded(suffixes=('_a', '_b'))
        complexes_composition = self.database_manager.get_repository('complex').get_all_compositions_expanded()

        return interactions_by_element.call(element, interactions, complexes_composition)

    def get_all_genes(self, columns: list = None) -> list:
        default_columns = ['ensembl', 'hgnc_symbol', 'gene_name']
        genes = self.database_manager.get_repository('gene').get_all()[columns or default_columns]
        return genes

    def get_complex_deconvoluted(self, complex_name: str) -> pd.DataFrame:
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions_expanded()

        complex_elements = complex_deconvoluted.call(complex_compositions, complex_name)
        return complex_elements
