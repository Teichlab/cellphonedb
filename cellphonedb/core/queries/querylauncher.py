import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.queries import cells_to_clusters, cluster_rl_permutations, cluster_rl_permutations_complex


class QueryLauncher():
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Launching Query {}'.format(name))

        return method

    def cells_to_clusters(self, meta, counts):
        genes = self.database_manager.get_repository('gene').get_all()
        return cells_to_clusters.call(meta, counts, genes)

    def get_multidatas_from_string(self, string: str) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(string)
        return multidatas

    def cluster_rl_permutations(self, meta: pd.DataFrame, count: pd.DataFrame, iterations: int, debug_seed: int) -> (
            pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return cluster_rl_permutations.call(meta, count, interactions, iterations, debug_seed)

    def cluster_rl_permutations_complex(self, meta: pd.DataFrame, count: pd.DataFrame, iterations: int,
                                        debug_seed) -> (pd.DataFrame, pd.DataFrame):
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()
        genes = self.database_manager.get_repository('gene').get_all_expanded()
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()

        return cluster_rl_permutations_complex.call(meta, count, interactions, genes, complex_expanded,
                                                    complex_composition, iterations, debug_seed)
