import pandas as pd

from cellphonedb.flask_app import output_dir, query_input_dir
from cellphonedb.extensions import cellphonedb_flask
from utils import utils


class FlaskTerminalQueryLauncher(object):
    def cells_to_clusters(self, meta_namefile, counts_namefile, data_path='', output_path='',
                          result_namefile='cells_to_clusters.csv'):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        result = cellphonedb_flask.cellphonedb.query.cells_to_clusters(meta, counts)

        result.to_csv('{}/{}'.format(output_path, result_namefile))

    def cluster_receptor_ligand_interactions(self, cluster_counts_namefile, threshold=0.2, enable_integrin: bool = True,
                                             enable_complex: bool = True, clusters=None, data_path='', output_path='',
                                             result_namefile='receptor_ligands_interactions.csv',
                                             result_extended_namefile='receptor_ligands_interactions_extended.csv'):
        if clusters:
            clusters = clusters.split(' ')

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        enable_integrin = bool(int(enable_integrin))
        enable_complex = bool(int(enable_complex))
        cluster_counts = utils.read_data_table_from_file('{}/{}'.format(data_path, cluster_counts_namefile),
                                                         index_column_first=True)

        result_interactions, result_interactions_extended = cellphonedb_flask.cellphonedb.query.cluster_receptor_ligand_interactions(
            cluster_counts, threshold, enable_integrin, enable_complex, clusters)

        result_interactions.to_csv('{}/{}'.format(output_path, result_namefile), index=False)
        result_interactions_extended.to_csv('{}/{}'.format(output_path, result_extended_namefile), index=False)

    def get_rl_lr_interactions(self, receptor, enable_secreted: str, enable_transmembrane: str, enable_integrin: str,
                               score2_threshold):

        enable_integrin = bool(int(enable_integrin))
        enable_transmembrane = bool(int(enable_transmembrane))
        enable_secreted = bool(int(enable_secreted))
        print(cellphonedb_flask.cellphonedb.query.get_rl_lr_interactions_from_multidata(
            receptor, enable_secreted, enable_transmembrane, enable_integrin, float(score2_threshold)))
