import pandas as pd

from cellphonedb.flask_app import output_dir, query_input_dir
from cellphonedb.extensions import cellphonedb_flask


class FlaskTerminalQueryLauncher(object):
    def cells_to_clusters(self, meta_namefile, counts_namefile, data_path='', output_path=''):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        counts = pd.read_csv('{}/{}'.format(data_path, counts_namefile), index_col=0)
        meta = pd.read_csv('{}/{}'.format(data_path, meta_namefile), index_col=0)

        result = cellphonedb_flask.cellphonedb.query.cells_to_clusters(meta, counts)

        result.to_csv('{}/cells_to_clusters.csv'.format(output_path))

    def receptor_ligand_secreted_interactions(self, cluster_counts_namefile, threshold=0.2,
                                              enable_complex: bool = True, data_path='', output_path=''):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        enable_complex = bool(int(enable_complex))
        cluster_counts = pd.read_table('{}/{}'.format(data_path, cluster_counts_namefile), index_col=0, sep=',')

        result_interactions, result_interactions_extended = cellphonedb_flask.cellphonedb.query.receptor_ligand_secreted_interactions(
            cluster_counts, threshold, enable_complex)

        result_interactions.to_csv('{}/receptor_ligand_secreted_interactions.csv'.format(output_path), index=False)
        result_interactions_extended.to_csv('{}/receptor_ligand_secreted_interactions_extended.csv'.format(output_path),
                                            index=False)

    def receptor_ligand_transmembrane_interactions(self, cluster_counts_namefile, threshold=0.2,
                                                   enable_complex: bool = True, data_path='', output_path=''):
        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        enable_complex = bool(int(enable_complex))
        cluster_counts = pd.read_table('{}/{}'.format(data_path, cluster_counts_namefile), index_col=0, sep=',')

        result_interactions, result_interactions_extended = cellphonedb_flask.cellphonedb.query.receptor_ligand_transmembrane_interactions(
            cluster_counts, threshold, enable_complex)

        result_interactions.to_csv('{}/receptor_ligand_transmembrane_interactions.csv'.format(output_path), index=False)
        result_interactions_extended.to_csv(
            '{}/receptor_ligand_transmembrane_interactions_extended.csv'.format(output_dir),
                                            index=False)

    # TODO: Remove me
    def receptor_ligands_interactions(self, cluster_counts_namefile, threshold=0.1, enable_integrin: bool = False,
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

    def get_rl_lr_interactions(self, receptor, score2_threshold):
        print(cellphonedb_flask.cellphonedb.get_rl_lr_interactions_from_multidata(receptor, float(score2_threshold)))
