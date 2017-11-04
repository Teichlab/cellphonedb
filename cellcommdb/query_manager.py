import pandas as pd

from cellcommdb.api import current_dir, output_dir
from cellcommdb.queries.query0 import Query0
from cellcommdb.queries.query1 import Query1
from cellcommdb.queries.query2 import Query2


class Queries(object):
    def __init__(self, app):
        self.app = app

    def query0(self):
        counts_namefile = 'test_counts.txt'
        meta_namefile = 'test_meta.txt'

        counts_df = pd.read_csv('%s/data/%s' % (current_dir, counts_namefile), sep='\t')
        meta_df = pd.read_csv('%s/data/%s' % (current_dir, meta_namefile), sep='\t')

        result_df = Query0.call(counts_df, meta_df)

        result_df.to_csv('%s/../out/query_0.csv' % current_dir, index=False)

    def query1(self):
        processed_data_namefile = 'query_0.csv'

        processed_data_df = pd.read_csv('%s/data/%s' % (current_dir, processed_data_namefile))

        result_df = Query1.call(processed_data_df)

        result_df.to_csv('%s/query_1.csv' % output_dir, index=False)

    def query2(self):
        query_1_namefile = 'query_1.csv'
        score_1 = 1
        score_2 = 2

        query_1_df = pd.read_csv('%s/data/%s' % (current_dir, query_1_namefile))

        Query2.call(query_1_df, score_1, score_2)
