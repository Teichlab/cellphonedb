import pandas as pd

from cellphonedb.core.queries import cells_to_clusters, cluster_receptor_ligand_interactions, \
    get_rl_lr_interactions_from_multidata


class QueryLauncher():
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def cells_to_clusters(self, meta, counts):
        genes = self.database_manager.get_repository('gene').get_all()
        return cells_to_clusters.call(meta, counts, genes)

    def cluster_receptor_ligand_interactions(self, cluster_counts, threshold, enable_integrin, enable_complex,
                                             clusters_names):
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()
        complex_expanded = complex_expanded[['id_multidata']]
        genes = self.database_manager.get_repository('gene').get_all_expanded()
        genes = genes[['ensembl', 'id_multidata']]
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return cluster_receptor_ligand_interactions.call(cluster_counts, threshold, enable_integrin, enable_complex,
                                                         complex_composition, genes, complex_expanded, interactions,
                                                         clusters_names)

    def get_rl_lr_interactions_from_multidata(self, receptor: str, enable_secreted: bool, enable_transmembrane: bool,
                                              enable_integrin: bool, score2_threshold: float) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(receptor)
        if multidatas.empty:
            return pd.DataFrame()
        interactions = self.database_manager.get_repository('interaction').get_all()
        multidatas_expanded = self.database_manager.get_repository('multidata').get_all()
        complex_by_multidata = self.database_manager.get_repository('complex').get_complex_by_multidatas(multidatas,
                                                                                                         False)

        result = pd.DataFrame()
        for index, multidata in multidatas.iterrows():
            multidata = multidata.to_frame().transpose()

            result = result.append(
                get_rl_lr_interactions_from_multidata.call(
                    multidata, enable_secreted, enable_transmembrane, enable_integrin, float(score2_threshold),
                    complex_by_multidata, interactions, multidatas_expanded),
                ignore_index=True)

        return result

    def get_multidatas_from_string(self, string: str) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(string)
        return multidatas
