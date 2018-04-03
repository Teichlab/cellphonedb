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
        cluster_counts = utils.read_data_table_from_file('{}/{}'.format(data_path, cluster_counts_namefile))

        result_interactions, result_interactions_extended = cellphonedb_flask.cellphonedb.query.cluster_receptor_ligand_interactions(
            cluster_counts, threshold, enable_integrin, enable_complex, clusters)

        result_interactions.to_csv('{}/{}'.format(output_path, result_namefile), index=False)
        result_interactions_extended.to_csv('{}/{}'.format(output_path, result_extended_namefile), index=False)

    def cluster_receptor_ligand_interactions_unprocessed(self, meta_namefile: str,
                                                         counts_namefile: str,
                                                         threshold: float = 0.2,
                                                         enable_integrin: bool = True,
                                                         enable_complex: bool = True, clusters=None, data_path='',
                                                         output_path: str = '',
                                                         result_cell_to_clusters_namefile: str = 'cells_to_clusters.csv',
                                                         result_interaction_namefile: str = 'receptor_ligands_interactions.csv',
                                                         result_interaction_extended_namefile: str = 'receptor_ligands_interactions_extended.csv'):

        if clusters:
            clusters = clusters.split(' ')
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        enable_integrin = bool(int(enable_integrin))
        enable_complex = bool(int(enable_complex))

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)
        cells_to_clusters_result = cellphonedb_flask.cellphonedb.query.cells_to_clusters(meta, counts)
        cells_to_clusters_result['gene'] = cells_to_clusters_result.index

        result_interactions, result_interactions_extended = cellphonedb_flask.cellphonedb.query.cluster_receptor_ligand_interactions(
            cells_to_clusters_result, threshold, enable_integrin, enable_complex, clusters)

        cells_to_clusters_result.to_csv('{}/{}'.format(output_path, result_cell_to_clusters_namefile), index=False)
        result_interactions.to_csv('{}/{}'.format(output_path, result_interaction_namefile), index=False)
        result_interactions_extended.to_csv('{}/{}'.format(output_path, result_interaction_extended_namefile),
                                            index=False)

    def get_rl_lr_interactions(self, receptor: str, enable_integrin: str = '1', min_score2: str = '0.2'):

        enable_integrin = bool(int(enable_integrin))
        print(cellphonedb_flask.cellphonedb.query.get_rl_lr_interactions_from_multidata(
            receptor, enable_integrin, float(min_score2)))
