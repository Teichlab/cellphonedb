from cellphonedb.app_logger import app_logger
from cellphonedb.flask_app import output_dir, query_input_dir
from cellphonedb.extensions import cellphonedb_flask
from utils import utils


class FlaskTerminalQueryLauncher(object):
    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            app_logger.info('Launching Query {}'.format(name))

        return method

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

    def human_interactions_permutations(self, meta_namefile: str, counts_namefile: str, iterations: str, data_path='',
                                        output_path: str = '', means_namefile: str = 'means_data.txt',
                                        pvalues_namefile: str = 'r_m_pvalues.txt', start_interaction: str = '0',
                                        how_many: str = '0', debug_mode: str = '0'):
        iterations = int(iterations)

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        start_interaction = int(start_interaction)
        how_many = int(how_many)
        debug_mode = bool(debug_mode)

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        means, pvalues = cellphonedb_flask.cellphonedb.query.human_interactions_permutations(meta, counts, iterations,
                                                                                             start_interaction,
                                                                                             how_many, debug_mode)

        means.to_csv('{}/{}'.format(output_path, means_namefile), sep='\t')
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_namefile), sep='\t')

    def cluster_rl_permutations(self, meta_namefile: str, counts_namefile: str, iterations: str, data_path='',
                                output_path: str = '', means_namefile: str = 'means.txt',
                                pvalues_namefile: str = 'pvalues.txt',
                                pvalues_means_namefile: str = 'pvalues_means.txt',
                                debug_mode: str = '0'):

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        debug_mode = bool(debug_mode)
        iterations = int(iterations)

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        pvalues, means, pvalues_means, pvalues_real = cellphonedb_flask.cellphonedb.query.cluster_rl_permutations(
            meta, counts, iterations, debug_mode)
        # TODO: Hardcoded lines for DEBUG (comparing results)
        means[['gene_interaction', 'EVT_EVT', 'EVT_dNK1', 'EVT_dNK2', 'EVT_dNK3', 'EVT_FB1', 'EVT_FB2', 'EVT_FB3',
               'EVT_FB4', 'EVT_FB5', 'EVT_CD8', 'EVT_CD4', 'EVT_Tregs', 'EVT_M1', 'EVT_M2', 'EVT_DC1', 'EVT_DC2',
               'EVT_Endothelial', 'EVT_Epithelial', 'dNK1_EVT', 'dNK1_dNK1', 'dNK1_dNK2', 'dNK1_dNK3', 'dNK1_FB1',
               'dNK1_FB2', 'dNK1_FB3', 'dNK1_FB4', 'dNK1_FB5', 'dNK1_CD8', 'dNK1_CD4', 'dNK1_Tregs', 'dNK1_M1',
               'dNK1_M2', 'dNK1_DC1', 'dNK1_DC2', 'dNK1_Endothelial', 'dNK1_Epithelial', 'dNK2_EVT', 'dNK2_dNK1',
               'dNK2_dNK2', 'dNK2_dNK3', 'dNK2_FB1', 'dNK2_FB2', 'dNK2_FB3', 'dNK2_FB4', 'dNK2_FB5', 'dNK2_CD8',
               'dNK2_CD4', 'dNK2_Tregs', 'dNK2_M1', 'dNK2_M2', 'dNK2_DC1', 'dNK2_DC2', 'dNK2_Endothelial',
               'dNK2_Epithelial', 'dNK3_EVT', 'dNK3_dNK1', 'dNK3_dNK2', 'dNK3_dNK3', 'dNK3_FB1', 'dNK3_FB2',
               'dNK3_FB3', 'dNK3_FB4', 'dNK3_FB5', 'dNK3_CD8', 'dNK3_CD4', 'dNK3_Tregs', 'dNK3_M1', 'dNK3_M2',
               'dNK3_DC1', 'dNK3_DC2', 'dNK3_Endothelial', 'dNK3_Epithelial', 'FB1_EVT', 'FB1_dNK1', 'FB1_dNK2',
               'FB1_dNK3', 'FB1_FB1', 'FB1_FB2', 'FB1_FB3', 'FB1_FB4', 'FB1_FB5', 'FB1_CD8', 'FB1_CD4', 'FB1_Tregs',
               'FB1_M1', 'FB1_M2', 'FB1_DC1', 'FB1_DC2', 'FB1_Endothelial', 'FB1_Epithelial', 'FB2_EVT', 'FB2_dNK1',
               'FB2_dNK2', 'FB2_dNK3', 'FB2_FB1', 'FB2_FB2', 'FB2_FB3', 'FB2_FB4', 'FB2_FB5', 'FB2_CD8', 'FB2_CD4',
               'FB2_Tregs', 'FB2_M1', 'FB2_M2', 'FB2_DC1', 'FB2_DC2', 'FB2_Endothelial', 'FB2_Epithelial', 'FB3_EVT',
               'FB3_dNK1', 'FB3_dNK2', 'FB3_dNK3', 'FB3_FB1', 'FB3_FB2', 'FB3_FB3', 'FB3_FB4', 'FB3_FB5', 'FB3_CD8',
               'FB3_CD4', 'FB3_Tregs', 'FB3_M1', 'FB3_M2', 'FB3_DC1', 'FB3_DC2', 'FB3_Endothelial', 'FB3_Epithelial',
               'FB4_EVT', 'FB4_dNK1', 'FB4_dNK2', 'FB4_dNK3', 'FB4_FB1', 'FB4_FB2', 'FB4_FB3', 'FB4_FB4', 'FB4_FB5',
               'FB4_CD8', 'FB4_CD4', 'FB4_Tregs', 'FB4_M1', 'FB4_M2', 'FB4_DC1', 'FB4_DC2', 'FB4_Endothelial',
               'FB4_Epithelial', 'FB5_EVT', 'FB5_dNK1', 'FB5_dNK2', 'FB5_dNK3', 'FB5_FB1', 'FB5_FB2', 'FB5_FB3',
               'FB5_FB4', 'FB5_FB5', 'FB5_CD8', 'FB5_CD4', 'FB5_Tregs', 'FB5_M1', 'FB5_M2', 'FB5_DC1', 'FB5_DC2',
               'FB5_Endothelial', 'FB5_Epithelial', 'CD8_EVT', 'CD8_dNK1', 'CD8_dNK2', 'CD8_dNK3', 'CD8_FB1',
               'CD8_FB2', 'CD8_FB3', 'CD8_FB4', 'CD8_FB5', 'CD8_CD8', 'CD8_CD4', 'CD8_Tregs', 'CD8_M1', 'CD8_M2',
               'CD8_DC1', 'CD8_DC2', 'CD8_Endothelial', 'CD8_Epithelial', 'CD4_EVT', 'CD4_dNK1', 'CD4_dNK2',
               'CD4_dNK3', 'CD4_FB1', 'CD4_FB2', 'CD4_FB3', 'CD4_FB4', 'CD4_FB5', 'CD4_CD8', 'CD4_CD4', 'CD4_Tregs',
               'CD4_M1', 'CD4_M2', 'CD4_DC1', 'CD4_DC2', 'CD4_Endothelial', 'CD4_Epithelial', 'Tregs_EVT',
               'Tregs_dNK1', 'Tregs_dNK2', 'Tregs_dNK3', 'Tregs_FB1', 'Tregs_FB2', 'Tregs_FB3', 'Tregs_FB4',
               'Tregs_FB5', 'Tregs_CD8', 'Tregs_CD4', 'Tregs_Tregs', 'Tregs_M1', 'Tregs_M2', 'Tregs_DC1', 'Tregs_DC2',
               'Tregs_Endothelial', 'Tregs_Epithelial', 'M1_EVT', 'M1_dNK1', 'M1_dNK2', 'M1_dNK3', 'M1_FB1', 'M1_FB2',
               'M1_FB3', 'M1_FB4', 'M1_FB5', 'M1_CD8', 'M1_CD4', 'M1_Tregs', 'M1_M1', 'M1_M2', 'M1_DC1', 'M1_DC2',
               'M1_Endothelial', 'M1_Epithelial', 'M2_EVT', 'M2_dNK1', 'M2_dNK2', 'M2_dNK3', 'M2_FB1', 'M2_FB2',
               'M2_FB3', 'M2_FB4', 'M2_FB5', 'M2_CD8', 'M2_CD4', 'M2_Tregs', 'M2_M1', 'M2_M2', 'M2_DC1', 'M2_DC2',
               'M2_Endothelial', 'M2_Epithelial', 'DC1_EVT', 'DC1_dNK1', 'DC1_dNK2', 'DC1_dNK3', 'DC1_FB1', 'DC1_FB2',
               'DC1_FB3', 'DC1_FB4', 'DC1_FB5', 'DC1_CD8', 'DC1_CD4', 'DC1_Tregs', 'DC1_M1', 'DC1_M2', 'DC1_DC1',
               'DC1_DC2', 'DC1_Endothelial', 'DC1_Epithelial', 'DC2_EVT', 'DC2_dNK1', 'DC2_dNK2', 'DC2_dNK3',
               'DC2_FB1', 'DC2_FB2', 'DC2_FB3', 'DC2_FB4', 'DC2_FB5', 'DC2_CD8', 'DC2_CD4', 'DC2_Tregs', 'DC2_M1',
               'DC2_M2', 'DC2_DC1', 'DC2_DC2', 'DC2_Endothelial', 'DC2_Epithelial', 'Endothelial_EVT',
               'Endothelial_dNK1', 'Endothelial_dNK2', 'Endothelial_dNK3', 'Endothelial_FB1', 'Endothelial_FB2',
               'Endothelial_FB3', 'Endothelial_FB4', 'Endothelial_FB5', 'Endothelial_CD8', 'Endothelial_CD4',
               'Endothelial_Tregs', 'Endothelial_M1', 'Endothelial_M2', 'Endothelial_DC1', 'Endothelial_DC2',
               'Endothelial_Endothelial', 'Endothelial_Epithelial', 'Epithelial_EVT', 'Epithelial_dNK1',
               'Epithelial_dNK2', 'Epithelial_dNK3', 'Epithelial_FB1', 'Epithelial_FB2', 'Epithelial_FB3',
               'Epithelial_FB4', 'Epithelial_FB5', 'Epithelial_CD8', 'Epithelial_CD4', 'Epithelial_Tregs',
               'Epithelial_M1', 'Epithelial_M2', 'Epithelial_DC1', 'Epithelial_DC2', 'Epithelial_Endothelial',
               'Epithelial_Epithelial']].to_csv('{}/{}'.format(output_path, means_namefile), sep='\t', index=False)
        pvalues[['gene_interaction', 'EVT_EVT', 'EVT_dNK1', 'EVT_dNK2', 'EVT_dNK3', 'EVT_FB1', 'EVT_FB2', 'EVT_FB3',
                 'EVT_FB4', 'EVT_FB5', 'EVT_CD8', 'EVT_CD4', 'EVT_Tregs', 'EVT_M1', 'EVT_M2', 'EVT_DC1', 'EVT_DC2',
                 'EVT_Endothelial', 'EVT_Epithelial', 'dNK1_EVT', 'dNK1_dNK1', 'dNK1_dNK2', 'dNK1_dNK3', 'dNK1_FB1',
                 'dNK1_FB2', 'dNK1_FB3', 'dNK1_FB4', 'dNK1_FB5', 'dNK1_CD8', 'dNK1_CD4', 'dNK1_Tregs', 'dNK1_M1',
                 'dNK1_M2', 'dNK1_DC1', 'dNK1_DC2', 'dNK1_Endothelial', 'dNK1_Epithelial', 'dNK2_EVT', 'dNK2_dNK1',
                 'dNK2_dNK2', 'dNK2_dNK3', 'dNK2_FB1', 'dNK2_FB2', 'dNK2_FB3', 'dNK2_FB4', 'dNK2_FB5', 'dNK2_CD8',
                 'dNK2_CD4', 'dNK2_Tregs', 'dNK2_M1', 'dNK2_M2', 'dNK2_DC1', 'dNK2_DC2', 'dNK2_Endothelial',
                 'dNK2_Epithelial', 'dNK3_EVT', 'dNK3_dNK1', 'dNK3_dNK2', 'dNK3_dNK3', 'dNK3_FB1', 'dNK3_FB2',
                 'dNK3_FB3', 'dNK3_FB4', 'dNK3_FB5', 'dNK3_CD8', 'dNK3_CD4', 'dNK3_Tregs', 'dNK3_M1', 'dNK3_M2',
                 'dNK3_DC1', 'dNK3_DC2', 'dNK3_Endothelial', 'dNK3_Epithelial', 'FB1_EVT', 'FB1_dNK1', 'FB1_dNK2',
                 'FB1_dNK3', 'FB1_FB1', 'FB1_FB2', 'FB1_FB3', 'FB1_FB4', 'FB1_FB5', 'FB1_CD8', 'FB1_CD4', 'FB1_Tregs',
                 'FB1_M1', 'FB1_M2', 'FB1_DC1', 'FB1_DC2', 'FB1_Endothelial', 'FB1_Epithelial', 'FB2_EVT', 'FB2_dNK1',
                 'FB2_dNK2', 'FB2_dNK3', 'FB2_FB1', 'FB2_FB2', 'FB2_FB3', 'FB2_FB4', 'FB2_FB5', 'FB2_CD8', 'FB2_CD4',
                 'FB2_Tregs', 'FB2_M1', 'FB2_M2', 'FB2_DC1', 'FB2_DC2', 'FB2_Endothelial', 'FB2_Epithelial', 'FB3_EVT',
                 'FB3_dNK1', 'FB3_dNK2', 'FB3_dNK3', 'FB3_FB1', 'FB3_FB2', 'FB3_FB3', 'FB3_FB4', 'FB3_FB5', 'FB3_CD8',
                 'FB3_CD4', 'FB3_Tregs', 'FB3_M1', 'FB3_M2', 'FB3_DC1', 'FB3_DC2', 'FB3_Endothelial', 'FB3_Epithelial',
                 'FB4_EVT', 'FB4_dNK1', 'FB4_dNK2', 'FB4_dNK3', 'FB4_FB1', 'FB4_FB2', 'FB4_FB3', 'FB4_FB4', 'FB4_FB5',
                 'FB4_CD8', 'FB4_CD4', 'FB4_Tregs', 'FB4_M1', 'FB4_M2', 'FB4_DC1', 'FB4_DC2', 'FB4_Endothelial',
                 'FB4_Epithelial', 'FB5_EVT', 'FB5_dNK1', 'FB5_dNK2', 'FB5_dNK3', 'FB5_FB1', 'FB5_FB2', 'FB5_FB3',
                 'FB5_FB4', 'FB5_FB5', 'FB5_CD8', 'FB5_CD4', 'FB5_Tregs', 'FB5_M1', 'FB5_M2', 'FB5_DC1', 'FB5_DC2',
                 'FB5_Endothelial', 'FB5_Epithelial', 'CD8_EVT', 'CD8_dNK1', 'CD8_dNK2', 'CD8_dNK3', 'CD8_FB1',
                 'CD8_FB2', 'CD8_FB3', 'CD8_FB4', 'CD8_FB5', 'CD8_CD8', 'CD8_CD4', 'CD8_Tregs', 'CD8_M1', 'CD8_M2',
                 'CD8_DC1', 'CD8_DC2', 'CD8_Endothelial', 'CD8_Epithelial', 'CD4_EVT', 'CD4_dNK1', 'CD4_dNK2',
                 'CD4_dNK3', 'CD4_FB1', 'CD4_FB2', 'CD4_FB3', 'CD4_FB4', 'CD4_FB5', 'CD4_CD8', 'CD4_CD4', 'CD4_Tregs',
                 'CD4_M1', 'CD4_M2', 'CD4_DC1', 'CD4_DC2', 'CD4_Endothelial', 'CD4_Epithelial', 'Tregs_EVT',
                 'Tregs_dNK1', 'Tregs_dNK2', 'Tregs_dNK3', 'Tregs_FB1', 'Tregs_FB2', 'Tregs_FB3', 'Tregs_FB4',
                 'Tregs_FB5', 'Tregs_CD8', 'Tregs_CD4', 'Tregs_Tregs', 'Tregs_M1', 'Tregs_M2', 'Tregs_DC1', 'Tregs_DC2',
                 'Tregs_Endothelial', 'Tregs_Epithelial', 'M1_EVT', 'M1_dNK1', 'M1_dNK2', 'M1_dNK3', 'M1_FB1', 'M1_FB2',
                 'M1_FB3', 'M1_FB4', 'M1_FB5', 'M1_CD8', 'M1_CD4', 'M1_Tregs', 'M1_M1', 'M1_M2', 'M1_DC1', 'M1_DC2',
                 'M1_Endothelial', 'M1_Epithelial', 'M2_EVT', 'M2_dNK1', 'M2_dNK2', 'M2_dNK3', 'M2_FB1', 'M2_FB2',
                 'M2_FB3', 'M2_FB4', 'M2_FB5', 'M2_CD8', 'M2_CD4', 'M2_Tregs', 'M2_M1', 'M2_M2', 'M2_DC1', 'M2_DC2',
                 'M2_Endothelial', 'M2_Epithelial', 'DC1_EVT', 'DC1_dNK1', 'DC1_dNK2', 'DC1_dNK3', 'DC1_FB1', 'DC1_FB2',
                 'DC1_FB3', 'DC1_FB4', 'DC1_FB5', 'DC1_CD8', 'DC1_CD4', 'DC1_Tregs', 'DC1_M1', 'DC1_M2', 'DC1_DC1',
                 'DC1_DC2', 'DC1_Endothelial', 'DC1_Epithelial', 'DC2_EVT', 'DC2_dNK1', 'DC2_dNK2', 'DC2_dNK3',
                 'DC2_FB1', 'DC2_FB2', 'DC2_FB3', 'DC2_FB4', 'DC2_FB5', 'DC2_CD8', 'DC2_CD4', 'DC2_Tregs', 'DC2_M1',
                 'DC2_M2', 'DC2_DC1', 'DC2_DC2', 'DC2_Endothelial', 'DC2_Epithelial', 'Endothelial_EVT',
                 'Endothelial_dNK1', 'Endothelial_dNK2', 'Endothelial_dNK3', 'Endothelial_FB1', 'Endothelial_FB2',
                 'Endothelial_FB3', 'Endothelial_FB4', 'Endothelial_FB5', 'Endothelial_CD8', 'Endothelial_CD4',
                 'Endothelial_Tregs', 'Endothelial_M1', 'Endothelial_M2', 'Endothelial_DC1', 'Endothelial_DC2',
                 'Endothelial_Endothelial', 'Endothelial_Epithelial', 'Epithelial_EVT', 'Epithelial_dNK1',
                 'Epithelial_dNK2', 'Epithelial_dNK3', 'Epithelial_FB1', 'Epithelial_FB2', 'Epithelial_FB3',
                 'Epithelial_FB4', 'Epithelial_FB5', 'Epithelial_CD8', 'Epithelial_CD4', 'Epithelial_Tregs',
                 'Epithelial_M1', 'Epithelial_M2', 'Epithelial_DC1', 'Epithelial_DC2', 'Epithelial_Endothelial',
                 'Epithelial_Epithelial']].to_csv('{}/{}'.format(output_path, pvalues_namefile), sep='\t', index=False)
        pvalues_means[
            ['gene_interaction', 'EVT_EVT', 'EVT_dNK1', 'EVT_dNK2', 'EVT_dNK3', 'EVT_FB1', 'EVT_FB2', 'EVT_FB3',
             'EVT_FB4', 'EVT_FB5', 'EVT_CD8', 'EVT_CD4', 'EVT_Tregs', 'EVT_M1', 'EVT_M2', 'EVT_DC1', 'EVT_DC2',
             'EVT_Endothelial', 'EVT_Epithelial', 'dNK1_EVT', 'dNK1_dNK1', 'dNK1_dNK2', 'dNK1_dNK3', 'dNK1_FB1',
             'dNK1_FB2', 'dNK1_FB3', 'dNK1_FB4', 'dNK1_FB5', 'dNK1_CD8', 'dNK1_CD4', 'dNK1_Tregs', 'dNK1_M1',
             'dNK1_M2', 'dNK1_DC1', 'dNK1_DC2', 'dNK1_Endothelial', 'dNK1_Epithelial', 'dNK2_EVT', 'dNK2_dNK1',
             'dNK2_dNK2', 'dNK2_dNK3', 'dNK2_FB1', 'dNK2_FB2', 'dNK2_FB3', 'dNK2_FB4', 'dNK2_FB5', 'dNK2_CD8',
             'dNK2_CD4', 'dNK2_Tregs', 'dNK2_M1', 'dNK2_M2', 'dNK2_DC1', 'dNK2_DC2', 'dNK2_Endothelial',
             'dNK2_Epithelial', 'dNK3_EVT', 'dNK3_dNK1', 'dNK3_dNK2', 'dNK3_dNK3', 'dNK3_FB1', 'dNK3_FB2',
             'dNK3_FB3', 'dNK3_FB4', 'dNK3_FB5', 'dNK3_CD8', 'dNK3_CD4', 'dNK3_Tregs', 'dNK3_M1', 'dNK3_M2',
             'dNK3_DC1', 'dNK3_DC2', 'dNK3_Endothelial', 'dNK3_Epithelial', 'FB1_EVT', 'FB1_dNK1', 'FB1_dNK2',
             'FB1_dNK3', 'FB1_FB1', 'FB1_FB2', 'FB1_FB3', 'FB1_FB4', 'FB1_FB5', 'FB1_CD8', 'FB1_CD4', 'FB1_Tregs',
             'FB1_M1', 'FB1_M2', 'FB1_DC1', 'FB1_DC2', 'FB1_Endothelial', 'FB1_Epithelial', 'FB2_EVT', 'FB2_dNK1',
             'FB2_dNK2', 'FB2_dNK3', 'FB2_FB1', 'FB2_FB2', 'FB2_FB3', 'FB2_FB4', 'FB2_FB5', 'FB2_CD8', 'FB2_CD4',
             'FB2_Tregs', 'FB2_M1', 'FB2_M2', 'FB2_DC1', 'FB2_DC2', 'FB2_Endothelial', 'FB2_Epithelial', 'FB3_EVT',
             'FB3_dNK1', 'FB3_dNK2', 'FB3_dNK3', 'FB3_FB1', 'FB3_FB2', 'FB3_FB3', 'FB3_FB4', 'FB3_FB5', 'FB3_CD8',
             'FB3_CD4', 'FB3_Tregs', 'FB3_M1', 'FB3_M2', 'FB3_DC1', 'FB3_DC2', 'FB3_Endothelial', 'FB3_Epithelial',
             'FB4_EVT', 'FB4_dNK1', 'FB4_dNK2', 'FB4_dNK3', 'FB4_FB1', 'FB4_FB2', 'FB4_FB3', 'FB4_FB4', 'FB4_FB5',
             'FB4_CD8', 'FB4_CD4', 'FB4_Tregs', 'FB4_M1', 'FB4_M2', 'FB4_DC1', 'FB4_DC2', 'FB4_Endothelial',
             'FB4_Epithelial', 'FB5_EVT', 'FB5_dNK1', 'FB5_dNK2', 'FB5_dNK3', 'FB5_FB1', 'FB5_FB2', 'FB5_FB3',
             'FB5_FB4', 'FB5_FB5', 'FB5_CD8', 'FB5_CD4', 'FB5_Tregs', 'FB5_M1', 'FB5_M2', 'FB5_DC1', 'FB5_DC2',
             'FB5_Endothelial', 'FB5_Epithelial', 'CD8_EVT', 'CD8_dNK1', 'CD8_dNK2', 'CD8_dNK3', 'CD8_FB1',
             'CD8_FB2', 'CD8_FB3', 'CD8_FB4', 'CD8_FB5', 'CD8_CD8', 'CD8_CD4', 'CD8_Tregs', 'CD8_M1', 'CD8_M2',
             'CD8_DC1', 'CD8_DC2', 'CD8_Endothelial', 'CD8_Epithelial', 'CD4_EVT', 'CD4_dNK1', 'CD4_dNK2',
             'CD4_dNK3', 'CD4_FB1', 'CD4_FB2', 'CD4_FB3', 'CD4_FB4', 'CD4_FB5', 'CD4_CD8', 'CD4_CD4', 'CD4_Tregs',
             'CD4_M1', 'CD4_M2', 'CD4_DC1', 'CD4_DC2', 'CD4_Endothelial', 'CD4_Epithelial', 'Tregs_EVT',
             'Tregs_dNK1', 'Tregs_dNK2', 'Tregs_dNK3', 'Tregs_FB1', 'Tregs_FB2', 'Tregs_FB3', 'Tregs_FB4',
             'Tregs_FB5', 'Tregs_CD8', 'Tregs_CD4', 'Tregs_Tregs', 'Tregs_M1', 'Tregs_M2', 'Tregs_DC1', 'Tregs_DC2',
             'Tregs_Endothelial', 'Tregs_Epithelial', 'M1_EVT', 'M1_dNK1', 'M1_dNK2', 'M1_dNK3', 'M1_FB1', 'M1_FB2',
             'M1_FB3', 'M1_FB4', 'M1_FB5', 'M1_CD8', 'M1_CD4', 'M1_Tregs', 'M1_M1', 'M1_M2', 'M1_DC1', 'M1_DC2',
             'M1_Endothelial', 'M1_Epithelial', 'M2_EVT', 'M2_dNK1', 'M2_dNK2', 'M2_dNK3', 'M2_FB1', 'M2_FB2',
             'M2_FB3', 'M2_FB4', 'M2_FB5', 'M2_CD8', 'M2_CD4', 'M2_Tregs', 'M2_M1', 'M2_M2', 'M2_DC1', 'M2_DC2',
             'M2_Endothelial', 'M2_Epithelial', 'DC1_EVT', 'DC1_dNK1', 'DC1_dNK2', 'DC1_dNK3', 'DC1_FB1', 'DC1_FB2',
             'DC1_FB3', 'DC1_FB4', 'DC1_FB5', 'DC1_CD8', 'DC1_CD4', 'DC1_Tregs', 'DC1_M1', 'DC1_M2', 'DC1_DC1',
             'DC1_DC2', 'DC1_Endothelial', 'DC1_Epithelial', 'DC2_EVT', 'DC2_dNK1', 'DC2_dNK2', 'DC2_dNK3',
             'DC2_FB1', 'DC2_FB2', 'DC2_FB3', 'DC2_FB4', 'DC2_FB5', 'DC2_CD8', 'DC2_CD4', 'DC2_Tregs', 'DC2_M1',
             'DC2_M2', 'DC2_DC1', 'DC2_DC2', 'DC2_Endothelial', 'DC2_Epithelial', 'Endothelial_EVT',
             'Endothelial_dNK1', 'Endothelial_dNK2', 'Endothelial_dNK3', 'Endothelial_FB1', 'Endothelial_FB2',
             'Endothelial_FB3', 'Endothelial_FB4', 'Endothelial_FB5', 'Endothelial_CD8', 'Endothelial_CD4',
             'Endothelial_Tregs', 'Endothelial_M1', 'Endothelial_M2', 'Endothelial_DC1', 'Endothelial_DC2',
             'Endothelial_Endothelial', 'Endothelial_Epithelial', 'Epithelial_EVT', 'Epithelial_dNK1',
             'Epithelial_dNK2', 'Epithelial_dNK3', 'Epithelial_FB1', 'Epithelial_FB2', 'Epithelial_FB3',
             'Epithelial_FB4', 'Epithelial_FB5', 'Epithelial_CD8', 'Epithelial_CD4', 'Epithelial_Tregs',
             'Epithelial_M1', 'Epithelial_M2', 'Epithelial_DC1', 'Epithelial_DC2', 'Epithelial_Endothelial',
             'Epithelial_Epithelial']].to_csv('{}/{}'.format(output_path, pvalues_means_namefile), sep='\t',
                                              index=False)

        ###DEBUG
        pvalues_real[pvalues_real['gene_interaction'] == 'CSF1R_CSF1'].to_csv(
            '{}/TEST_pvalues_real.csv'.format(output_path, pvalues_means_namefile), sep='\t', index=False)

    def cluster_rl_permutations_complex(self, meta_namefile: str, counts_namefile: str, iterations: str, data_path='',
                                        output_path: str = '', means_namefile: str = 'means.txt',
                                        pvalues_namefile: str = 'pvalues.txt', debug_mode: str = '0'):

        if not data_path:
            data_path = query_input_dir
        if not output_path:
            output_path = output_dir

        debug_mode = bool(debug_mode)
        iterations = int(iterations)

        meta = utils.read_data_table_from_file('{}/{}'.format(data_path, meta_namefile), index_column_first=True)
        counts = utils.read_data_table_from_file('{}/{}'.format(data_path, counts_namefile), index_column_first=True)

        means, pvalues = cellphonedb_flask.cellphonedb.query.cluster_rl_permutations_complex(meta, counts, iterations,
                                                                                             debug_mode)

        means.to_csv('{}/{}'.format(output_path, means_namefile), sep='\t')
        pvalues.to_csv('{}/{}'.format(output_path, pvalues_namefile), sep='\t')
