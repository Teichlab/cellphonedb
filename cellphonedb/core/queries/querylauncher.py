import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.queries import cells_to_clusters, cluster_receptor_ligand_interactions, \
    get_rl_lr_interactions_from_multidata, human_interactions_permutations


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

    def cluster_receptor_ligand_interactions(self, cluster_counts, threshold, enable_integrin, enable_complex,
                                             clusters_names):
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()
        genes = self.database_manager.get_repository('gene').get_all_expanded()
        interactions = self.database_manager.get_repository('interaction').get_all()

        return cluster_receptor_ligand_interactions.call(cluster_counts, threshold, enable_integrin, enable_complex,
                                                         complex_composition, genes, complex_expanded, interactions,
                                                         clusters_names)

    def get_rl_lr_interactions_from_multidata(self, receptor: str,
                                              enable_integrin: bool, min_score2: float) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(receptor)
        if multidatas.empty:
            return pd.DataFrame()

        multidatas.drop_duplicates('id_multidata', inplace=True)
        interactions = self.database_manager.get_repository('interaction').get_all()
        multidatas_expanded = self.database_manager.get_repository('multidata').get_all_expanded()
        complex_by_multidata = self.database_manager.get_repository('complex').get_complex_by_multidatas(multidatas,
                                                                                                         False)

        result = pd.DataFrame()
        for index, multidata in multidatas.iterrows():
            multidata = multidata.to_frame().transpose()

            result = result.append(
                get_rl_lr_interactions_from_multidata.call(
                    multidata, enable_integrin, float(min_score2),
                    complex_by_multidata, interactions, multidatas_expanded),
                ignore_index=True)

        return result

    def get_multidatas_from_string(self, string: str) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(string)
        return multidatas

    def human_interactions_permutations(self, meta: pd.DataFrame, counts: pd.DataFrame, iterations: int,
                                        start_interaction: int, how_many: int, debug_mode: bool) \
            -> (pd.DataFrame, pd.DataFrame):

        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return human_interactions_permutations.call(meta, counts, interactions, iterations, start_interaction,
                                                    how_many, debug_mode)
