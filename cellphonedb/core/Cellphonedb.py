import pandas as pd

from cellphonedb.core.collectors.collectorlauncher import CollectorLauncher
from cellphonedb.core.exporters.exporterlauncher import ExporterLauncher
from cellphonedb.database import DatabaseManager
from cellphonedb.queries import cells_to_clusters, receptor_ligands_interactions, \
    get_rl_lr_interactions_from_multidata


class Cellphonedb(object):
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        self.export = ExporterLauncher(self.database_manager)
        self.collect = CollectorLauncher(self.database_manager)

    def cells_to_clusters(self, counts, meta):
        genes = self.database_manager.get_repository('gene').get_all()
        return cells_to_clusters.call(counts, meta, genes)

    def receptor_ligands_interactions(self, cluster_counts, threshold, enable_integrin, enable_complex, clusters_names):
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()
        genes_expanded = self.database_manager.get_repository('gene').get_all_expanded()
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return receptor_ligands_interactions.call(cluster_counts, threshold, enable_integrin, enable_complex,
                                                  complex_composition, genes_expanded, complex_expanded, interactions,
                                                  clusters_names)

    def get_rl_lr_interactions_from_multidata(self, receptor: str, score2_threshold: float):
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(receptor)
        interactions = self.database_manager.get_repository('interaction').get_all()
        multidatas_expanded = self.database_manager.get_repository('multidata').get_all_expanded()
        complex_by_multidata = self.database_manager.get_repository('complex').get_complex_by_multidatas(multidatas,
                                                                                                         False)

        results = []
        for index, multidata in multidatas.iterrows():
            multidata = multidata.to_frame().transpose()
            results.append(
                get_rl_lr_interactions_from_multidata.call(multidata, float(score2_threshold), complex_by_multidata,
                                                           interactions, multidatas_expanded))

        return results

    def get_multidatas_from_string(self, string: str) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(string)
        return multidatas
