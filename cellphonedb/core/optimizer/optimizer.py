from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.optimizer import protein_optimizer, complex_optimizer
from cellphonedb.core.database import DatabaseManager


class Optimizer():
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Launching Optimizer {}'.format(name))

        return method

    def protein(self):
        multidatas = self.database_manager.get_repository('multidata').get_all_expanded(include_gene=False)
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return protein_optimizer.call(multidatas, interactions)

    def complex(self):
        multidatas = self.database_manager.get_repository('multidata').get_all_expanded(include_gene=False)
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()
        complexes = self.database_manager.get_repository('complex').get_all()
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions()
        proteins = self.database_manager.get_repository('protein').get_all_expanded()

        multidata_column_names = self.database_manager.get_column_table_names('multidata')
        return complex_optimizer.call(multidatas, interactions, multidata_column_names, complexes, complex_compositions,
                                      proteins)
