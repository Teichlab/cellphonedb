import pandas as pd
from flask import request, Response

from cellcommdb.api_endpoints.queries.query_base import QueryBase
from cellcommdb.queries import cells_to_clusters


# curl -i \
#     -F "counts_file=@cellcommdb/data/queries/test_counts.txt;type=text/tab-separated-values" \
#     -F "meta_file=@cellcommdb/data/queries/test_meta.txt;type=text/tab-separated-values" \
#     http://127.0.0.1:5000/api/cell_to_cluster


class CellToCluster(QueryBase):
    def post(self):
        counts = self._read_table(request.files['counts_file'], index_column_first=True)
        meta = self._read_table(request.files['meta_file'], index_column_first=True)

        if not isinstance(counts, pd.DataFrame):
            self._status['error'] = True
            self._status['errors'].append('Counts file is not well formed')

        if not isinstance(meta, pd.DataFrame):
            self._status['error'] = True
            self._status['errors'].append('Meta file is not well formed')

        if not self._status['error']:
            result_df = cells_to_clusters.call(counts, meta)

            self._attach_csv(result_df.to_csv(), 'cluster_counts.csv')

        self._attach_json(self._status, at_first=True)
        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
