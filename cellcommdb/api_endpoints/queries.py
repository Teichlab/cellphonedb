from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from flask import request, Response
from flask_restful import Resource, reqparse
from cellcommdb.queries import cells_to_clusters, receptor_ligands_interactions


# Example queries
# Query CellToCluster
# curl -i \
#     -F counts_file=@cellcommdb/data/queries/test_counts.txt \
#     -F meta_file=@cellcommdb/data/queries/test_meta.txt \
#     http://127.0.0.1:5000/api/cell_to_cluster


# Query ReceptorLigandsInteractions
# curl -i \
#     -F cells_to_clusters=@cellcommdb/data/queries/cells_to_clusters.csv \
#     http://127.0.0.1:5000/api/receptor_ligands_interactions

class QueryBase(Resource):
    def __init__(self):
        self.msg = MIMEMultipart('multipart')

    def _attach_file(self, file_to_send):
        file_attach = MIMEText(file_to_send, 'plain')
        self.msg.attach(file_attach)


class CellToCluster(QueryBase):
    def post(self):
        counts = pd.read_table(request.files['counts_file'].stream, index_col=0)
        meta = pd.read_table(request.files['meta_file'].stream, index_col=0)
        result_df = cells_to_clusters.call(counts, meta)

        self._attach_file(result_df.to_csv(sep='\t'))
        return Response(self.msg.as_string())


class ReceptorLigandsInteractions(QueryBase):
    def post(self):
        cells_to_clusters_file = pd.read_csv(request.files['cells_to_clusters'].stream, index_col=0)

        result_interactions, result_interactions_extended = receptor_ligands_interactions.call(cells_to_clusters_file)

        self._attach_file(result_interactions.to_csv(sep='\t'))
        self._attach_file(result_interactions_extended.to_csv(sep='\t'))

        return Response(self.msg.as_string())
