import mimetypes
from email import encoders

import pandas as pd

from cellcommdb.api import current_dir, output_dir, query_input_dir
from cellcommdb.queries.query0 import Query0
from cellcommdb.queries.query1 import Query1

from cellcommdb.queries import complexes, one_one, cells_to_clusters, \
    receptor_ligands_interactions, get_rl_lr_interactions_from_multidata
from cellcommdb.repository import multidata_repository


class QueryLauncher(object):
    def __init__(self, app):
        self.app = app

    def query0(self, counts_namefile, meta_namefile):
        counts_df = pd.read_csv('%s/%s' % (query_input_dir, counts_namefile), sep='\t')
        meta_df = pd.read_csv('%s/%s' % (query_input_dir, meta_namefile), sep='\t')

        result_df = Query0.call(counts_df, meta_df)

        result_df.to_csv('%squery_0.csv' % output_dir, index=False)

    def query1(self, processed_data_namefile):
        processed_data_namefile = 'query_0.csv'

        processed_data_df = pd.read_csv('%s/data/%s' % (current_dir, processed_data_namefile))

        result_df = Query1.call(processed_data_df)

        result_df.to_csv('%s/query_1.csv' % output_dir, index=False)

    def complexes(self, counts_namefile, meta_namefile):
        counts = pd.read_table('%s/%s' % (query_input_dir, counts_namefile), index_col=0)
        meta = pd.read_table('%s/%s' % (query_input_dir, meta_namefile), index_col=0)
        complexes.call(counts, meta)

    def one_one(self, counts_namefile, meta_namefile):
        counts = pd.read_table('%s/%s' % (query_input_dir, counts_namefile), index_col=0)
        meta = pd.read_table('%s/%s' % (query_input_dir, meta_namefile), index_col=0)
        one_one.call(counts, meta)

    def cells_to_clusters(self, counts_namefile, meta_namefile):
        counts = pd.read_table('%s/%s' % (query_input_dir, counts_namefile), index_col=0)
        meta = pd.read_table('%s/%s' % (query_input_dir, meta_namefile), index_col=0)

        result = cells_to_clusters.call(counts, meta)

        result.to_csv('%s/cells_to_clusters.csv' % (output_dir))

    def receptor_ligands_interactions(self, cluster_counts_namefile, threshold=0.1):
        cluster_counts = pd.read_table('%s/%s' % (query_input_dir, cluster_counts_namefile), index_col=0, sep=',')

        result_interactions, result_interactions_extended = receptor_ligands_interactions.call(cluster_counts,
                                                                                               threshold)

        result_interactions.to_csv('%s/receptor_ligands_interactions.csv' % output_dir, index=False)
        result_interactions_extended.to_csv('%s/receptor_ligands_interactions_extended.csv' % output_dir, index=False)

    def get_ligands_from_receptor(self, receptor, score2_threshold):
        multidatas_receptor = multidata_repository.get_multidatas_from_string(receptor)

        for index, multidata_receptor in multidatas_receptor.iterrows():
            print(get_rl_lr_interactions_from_multidata.call(multidata_receptor, float(score2_threshold)))
