import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.database import DatabaseManager
from cellphonedb.core.queries.complex import complex_deconvoluted
from cellphonedb.core.queries.interaction import interaction_gene_get, interactions_by_element
from cellphonedb.core.queries.reports import cpdb_data_report_query


class QueryLauncher:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def __getattribute__(self, name: str):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Launching Query {}'.format(name))

        return method

    def find_interactions_by_element(self, element: str) -> pd.DataFrame:
        interactions = self.database_manager.get_repository('interaction').get_all_expanded(suffixes=('_a', '_b'))
        complexes_composition = self.database_manager.get_repository('complex').get_all_compositions_expanded()

        return interactions_by_element.call(element, interactions, complexes_composition)

    def get_interaction_gene(self, columns: list = None) -> pd.DataFrame:
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions_expanded()

        genes = interaction_gene_get.call(columns, interactions, complex_composition)

        return genes

    def cpdb_data_report_launcher(self) -> {}:
        proteins = self.database_manager.get_repository('protein').get_all_expanded()
        interactions = self.database_manager.get_repository('interaction').get_all_expanded(include_gene=False)
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions()

        report = cpdb_data_report_query.call(complex_compositions, interactions, proteins)

        return report

    def get_complex_deconvoluted(self, complex_name: str) -> pd.DataFrame:
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions_expanded()

        complex_elements = complex_deconvoluted.call(complex_compositions, complex_name)
        return complex_elements
