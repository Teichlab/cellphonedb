import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.database import DatabaseManager
from cellphonedb.core.queries import interactions_by_component
from cellphonedb.core.queries.interaction import interaction_gene_get


class QueryLauncher:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def __getattribute__(self, name: str):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Launching Query {}'.format(name))

        return method

    def search_interactions(self, input: str) -> pd.DataFrame:
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()
        return interactions_by_component.call(input, interactions)

    def get_interaction_gene(self, columns: list = None) -> pd.DataFrame:
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions_expanded()

        genes = interaction_gene_get.call(columns, interactions, complex_composition)

        return genes
