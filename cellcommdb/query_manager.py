import pandas as pd

from cellcommdb.api import current_dir, output_dir, data_dir
from cellcommdb.queries.query0 import Query0
from cellcommdb.queries.query1 import Query1
from cellcommdb.queries.query2 import Query2


class Queries(object):
    def __init__(self, app):
        self.app = app

    def query0(self, counts_namefile, meta_namefile):
        counts_df = pd.read_csv('%s%s' % (data_dir, counts_namefile), sep='\t')
        meta_df = pd.read_csv('%s%s' % (data_dir, meta_namefile), sep='\t')

        result_df = Query0.call(counts_df, meta_df)

        result_df.to_csv('%squery_0.csv' % output_dir, index=False)

    def query1(self, processed_data_namefile):
        processed_data_namefile = 'query_0.csv'

        processed_data_df = pd.read_csv('%s/data/%s' % (current_dir, processed_data_namefile))

        result_df = Query1.call(processed_data_df)

        result_df.to_csv('%s/query_1.csv' % output_dir, index=False)

    def query2(self, query_1_result_namefile, score_1, score_2):
        query_1_df = pd.read_csv('%s/data/%s' % (current_dir, query_1_result_namefile))

        Query2.call(query_1_df, score_1, score_2)
