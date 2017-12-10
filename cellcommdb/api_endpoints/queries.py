from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import pandas as pd
from flask import request, Response
from flask_restful import Resource
from cellcommdb.queries import cells_to_clusters, receptor_ligands_interactions

import json


# Example queries
# Query CellToCluster
# curl -i \
#     -F "counts_file=@cellcommdb/data/queries/test_counts.txt;type=text/tab-separated-values" \
#     -F "meta_file=@cellcommdb/data/queries/test_meta.txt;type=text/tab-separated-values" \
#     http://127.0.0.1:5000/api/cell_to_cluster


# Query ReceptorLigandsInteractions
# curl -i \
#      -F "cell_to_clusters_file=@cellcommdb/data/queries/cells_to_clusters.csv;type=text/csv" \
#      -F parameters="{\"threshold\": 0.1}" \
#      http://127.0.0.1:5000/api/receptor_ligands_interactions


class QueryBase(Resource):
    def __init__(self):
        self._msg = MIMEMultipart('form-data')
        self._status = {'status': 'ok', 'error': False, 'errors': []}
        self._attachments = []

    def _attach_csv(self, file_to_send, filename):
        attachment = MIMEBase('text', 'csv')
        attachment.set_payload(file_to_send)

        attachment.add_header("Content-Disposition", "attachment", filename=filename)

        self._attachments.append(attachment)

    def _attach_json(self, data, at_first=False):
        attachment = MIMEBase('application', 'json')
        attachment.set_payload(json.dumps(data))

        if at_first:
            self._attachments = [attachment] + self._attachments

        else:
            self._attachments.append(attachment)

    def _commit_attachments(self):
        for attach in self._attachments:
            self._msg.attach(attach)

    def _read_table(self, file, index_column_first=False):

        if file.content_type == 'text/csv':
            return pd.read_csv(file.stream, index_col=0 if index_column_first else None)

        if file.content_type == 'text/tab-separated-values':
            return pd.read_table(file.stream, index_col=0 if index_column_first else None)

        return None


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


class ReceptorLigandsInteractions(QueryBase):
    def post(self):
        cells_to_clusters_file = self._read_table(request.files['cell_to_clusters_file'], True)

        if not isinstance(cells_to_clusters_file, pd.DataFrame):
            self._status['status'] = 'error'
            self._status['error'] = True

        if not self._status['error']:
            parameters = json.loads(request.form['parameters'])
            threshold = float(parameters['threshold'])

            result_interactions, result_interactions_extended = receptor_ligands_interactions.call(
                cells_to_clusters_file,
                threshold)
            self._attach_csv(result_interactions.to_csv(sep='\t', index=False), 'result_interactions.txt')
            self._attach_csv(result_interactions_extended.to_csv(sep='\t', index=False),
                             'result_interactions_extended.txt')

        self._attach_json(self._status, at_first=True)

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
