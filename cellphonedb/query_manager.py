import pandas as pd

from cellphonedb.api import current_dir, output_dir, query_input_dir

from cellphonedb.queries import cells_to_clusters, \
    receptor_ligands_interactions, get_rl_lr_interactions_from_multidata
from cellphonedb.repository import multidata_repository


class QueryLauncher(object):
    def __init__(self, app):
        self.app = app

    def cells_to_clusters(self, counts_namefile, meta_namefile):
        counts = pd.read_table('%s/%s' % (query_input_dir, counts_namefile), index_col=0)
        meta = pd.read_table('%s/%s' % (query_input_dir, meta_namefile), index_col=0)

        result = cells_to_clusters.call(counts, meta)

        result.to_csv('%s/cells_to_clusters.csv' % (output_dir))

    def receptor_ligands_interactions(self, cluster_counts_namefile, threshold=0.1, enable_integrin=False):
        cluster_counts = pd.read_table('%s/%s' % (query_input_dir, cluster_counts_namefile), index_col=0, sep=',')

        result_interactions, result_interactions_extended = receptor_ligands_interactions.call(cluster_counts,
                                                                                               threshold,
                                                                                               enable_integrin)

        result_interactions.to_csv('%s/receptor_ligands_interactions.csv' % output_dir, index=False)
        result_interactions_extended.to_csv('%s/receptor_ligands_interactions_extended.csv' % output_dir, index=False)

    def get_rl_lr_interactions(self, receptor, score2_threshold):
        multidatas_receptor = multidata_repository.get_multidatas_from_string(receptor)

        for index, multidata_receptor in multidatas_receptor.iterrows():
            print(get_rl_lr_interactions_from_multidata.call(multidata_receptor, float(score2_threshold)))
