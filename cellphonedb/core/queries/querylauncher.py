import pandas as pd

from cellphonedb.core.queries import cells_to_clusters, receptor_ligands_interactions, \
    get_rl_lr_interactions_from_multidata, receptor_ligand_secreted_interactions


class QueryLauncher():
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def cells_to_clusters(self, meta, counts):
        genes = self.database_manager.get_repository('gene').get_all()
        return cells_to_clusters.call(meta, counts, genes)

    def receptor_ligand_secreted_interactions(self, cluster_counts, threshold, enable_complex):
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()
        genes_expanded = self.database_manager.get_repository('gene').get_all_expanded()
        interactions_expanded = self.database_manager.get_repository('interaction').get_all_expanded()
        return receptor_ligand_secreted_interactions.call(cluster_counts, threshold, enable_complex,
                                                          complex_composition, genes_expanded, complex_expanded,
                                                          interactions_expanded)

    def receptor_ligands_interactions(self, cluster_counts, threshold, enable_integrin, enable_complex, clusters_names):
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()
        genes_expanded = self.database_manager.get_repository('gene').get_all_expanded()
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return receptor_ligands_interactions.call(cluster_counts, threshold, enable_integrin, enable_complex,
                                                  complex_composition, genes_expanded, complex_expanded, interactions,
                                                  clusters_names)

    def get_rl_lr_interactions_from_multidata(self, receptor: str, score2_threshold: float) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(receptor)
        if multidatas.empty:
            return pd.DataFrame()
        interactions = self.database_manager.get_repository('interaction').get_all()
        multidatas_expanded = self.database_manager.get_repository('multidata').get_all_expanded()
        complex_by_multidata = self.database_manager.get_repository('complex').get_complex_by_multidatas(multidatas,
                                                                                                         False)

        result = pd.DataFrame()
        for index, multidata in multidatas.iterrows():
            multidata = multidata.to_frame().transpose()

            result = result.append(
                get_rl_lr_interactions_from_multidata.call(multidata, float(score2_threshold), complex_by_multidata,
                                                           interactions, multidatas_expanded),
                ignore_index=True)

        return result

    def get_multidatas_from_string(self, string: str) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(string)
        return multidatas
