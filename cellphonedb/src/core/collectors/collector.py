import pandas as pd

from cellphonedb.src.core.collectors import protein_preprocess_collector, gene_preprocess_collector, \
    complex_preprocess_collector, interaction_preprocess_collector
from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.database import DatabaseManager


class Collector(object):
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def __getattribute__(self, name: str):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Collecting {}'.format(name))

        return method

    def protein(self, proteins: pd.DataFrame):
        multidata_columns = self.database_manager.get_column_table_names('multidata_table')
        protein_columns = self.database_manager.get_column_table_names('protein_table')

        proteins_to_add, multidata_to_add = protein_preprocess_collector.call(proteins, multidata_columns,
                                                                              protein_columns)

        self.database_manager.get_repository('protein').add_proteins(proteins_to_add, multidata_to_add)

    def gene(self, genes: pd.DataFrame):
        genes_processed = gene_preprocess_collector.call(genes,
                                                         self.database_manager.get_column_table_names('gene_table'))
        self.database_manager.get_repository('gene').add(genes_processed)

    def complex(self, complexes: pd.DataFrame):
        complexes_processed = complex_preprocess_collector.call(complexes)
        self.database_manager.get_repository('complex').add(complexes_processed)

    def interaction(self, interactions: pd.DataFrame):
        multidatas = self.database_manager.get_repository('multidata').get_all_expanded(include_gene=False)
        interactions_processed = interaction_preprocess_collector.call(interactions, multidatas)
        self.database_manager.get_repository('interaction').add(interactions_processed)

    def all(self, proteins: pd.DataFrame, genes: pd.DataFrame, complexes: pd.DataFrame, interactions: pd.DataFrame):
        self.protein(proteins)
        self.gene(genes)
        self.complex(complexes)
        self.interaction(interactions)
