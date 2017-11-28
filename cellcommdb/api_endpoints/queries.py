import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import requests
from flask import request, Response
from flask_restful import Resource, reqparse
from cellcommdb.queries import cells_to_clusters, receptor_ligands_interactions

parser = reqparse.RequestParser()
parser.add_argument('meta')
parser.add_argument('counts')


# Example query
# Query CellToCluster
# curl -i \
#     -F counts_file=@cellcommdb/data/queries/test_counts.txt \
#     -F meta_file=@cellcommdb/data/queries/test_meta.txt \
#     http://127.0.0.1:5000/api/cell_to_cluster

class QueryBase(Resource):
    # def _add_file_to_multipart(self, file_to_send):
    # response_body = MIMEMultipart()
    # file_to_send = 'cellcommdb/data/queries/test_meta.txt'
    # ctype, encoding = mimetypes.guess_type(file_to_send)
    # if ctype is None or encoding is not None:
    #     ctype = "application/octet-stream"
    #
    # maintype, subtype = ctype.split("/", 1)
    # file = open(file_to_send, "rb")
    # attachment = MIMEBase(maintype, subtype)
    # attachment.set_payload(file.read())
    # file.close()
    # encoders.encode_base64(attachment)
    #
    # attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)
    # response_body.attach(attachment)

    def _add_file_to_multipart(self, file_to_send):
        msg = MIMEMultipart('multipart')

        file_attach = MIMEText(file_to_send, 'plain')
        msg.attach(file_attach)

        return msg


class CellToCluster(QueryBase):
    def post(self):
        counts = pd.read_table(request.files['counts_file'].stream, index_col=0)
        meta = pd.read_table(request.files['meta_file'].stream, index_col=0)
        result_df = cells_to_clusters.call(counts, meta)
        # mimetype='text/csv'

        response_multipart = self._add_file_to_multipart(result_df.to_csv(sep='\t'))
        return Response(response_multipart.as_string())


class ReceptorLigandsInteractions(Resource):
    def post(self):
        counts = pd.read_table(request.files['counts_file'].stream, index_col=0)
        meta = pd.read_table(request.files['meta_file'].stream, index_col=0)

        result_df = receptor_ligands_interactions.call(counts, meta)

        return Response(result_df.to_csv(sep='\t'), mimetype='text/csv')
