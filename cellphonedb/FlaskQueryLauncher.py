import pandas as pd

from cellphonedb.api import output_dir, query_input_dir
from cellphonedb.extensions import cellphonedb_flask


class FlaskQueryLauncher(object):
    @staticmethod
    def cells_to_clusters(counts_namefile, meta_namefile):
        counts = pd.read_table('%s/%s' % (query_input_dir, counts_namefile), index_col=0)
        meta = pd.read_table('%s/%s' % (query_input_dir, meta_namefile), index_col=0)

        result = cellphonedb_flask.cellphonedb.cells_to_clusters(counts, meta)

        result.to_csv('%s/cells_to_clusters.csv' % (output_dir))

    @staticmethod
    def receptor_ligands_interactions(cluster_counts_namefile, threshold=0.1, enable_integrin: bool = False,
                                      enable_complex: bool = True, clusters=None):
        if clusters:
            clusters = clusters.split(' ')

        enable_integrin = bool(int(enable_integrin))
        enable_complex = bool(int(enable_complex))
        cluster_counts = pd.read_table('%s/%s' % (query_input_dir, cluster_counts_namefile), index_col=0, sep=',')

        result_interactions, result_interactions_extended = cellphonedb_flask.cellphonedb.receptor_ligands_interactions(
            cluster_counts, threshold, enable_integrin, enable_complex, clusters)

        result_interactions.to_csv('%s/receptor_ligands_interactions.csv' % output_dir, index=False)
        result_interactions_extended.to_csv('%s/receptor_ligands_interactions_extended.csv' % output_dir, index=False)

    @staticmethod
    def get_rl_lr_interactions(receptor, score2_threshold):
        print(cellphonedb_flask.cellphonedb.get_rl_lr_interactions_from_multidata(receptor, float(score2_threshold)))
