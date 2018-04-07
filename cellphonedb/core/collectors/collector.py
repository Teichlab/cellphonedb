from cellphonedb.core.collectors import protein_preprocess_collector, gene_preprocess_collector, \
    complex_preprocess_collector
from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.database import DatabaseManager


class Collector(object):
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Collecting {}'.format(name))

        return method

    def protein(self, proteins):
        multidata_columns = self.database_manager.get_column_table_names('multidata')
        protein_columns = self.database_manager.get_column_table_names('protein')

        proteins_to_add, multidata_to_add = protein_preprocess_collector.call(proteins, multidata_columns,
                                                                              protein_columns)

        self.database_manager.get_repository('protein').add_proteins(proteins_to_add, multidata_to_add)

    def gene(self, genes):
        genes_processed = gene_preprocess_collector.call(genes, self.database_manager.get_column_table_names('gene'))
        self.database_manager.get_repository('gene').add(genes_processed)

    def complex(self, complexes):
        complexes_processed = complex_preprocess_collector.call(complexes)
        self.database_manager.get_repository('complex').add(complexes_processed)

    def interaction(self, interactions):
        self.database_manager.get_repository('interaction').add(interactions)

    def all(self, proteins, genes, complexes, interactions):
        self.protein(proteins)
        self.gene(genes)
        self.complex(complexes)
        self.interaction(interactions)
