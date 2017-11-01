import pandas as pd

from cellcommdb.api import current_dir
from cellcommdb.queries.query0 import Query0


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
