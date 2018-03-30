import json

import pandas as pd
from flask import request, Response

from cellphonedb import extensions
from cellphonedb.api_endpoints.endpoint_base import EndpointBase


# curl -i \
#     -F "counts_file=@in/example_data/test_counts.txt;type=text/tab-separated-values" \
#     -F "meta_file=@in/example_data/test_meta.txt;type=text/tab-separated-values" \
#     -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
#     http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions_unprocessed


class ClusterReceptorLigandInteractionsUnprocessed(EndpointBase):
    def post(self):

        meta = self._read_table(request.files['meta_file'], index_column_first=True)
        counts = self._read_table(request.files['counts_file'], index_column_first=True)

        if not isinstance(counts, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing counts file', 'detail': 'Error parsing counts file'})

        if not isinstance(meta, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing meta file', 'detail': 'Error parsing meta file'})

        if not self._errors:
            cells_to_clusters_result = extensions.cellphonedb_flask.cellphonedb.query.cells_to_clusters(meta, counts)
            cells_to_clusters_result['gene'] = cells_to_clusters_result.index
            cells_to_clusters_result.reset_index(drop=True, inplace=True)
            parameters = json.loads(request.form['parameters'])
            threshold = float(parameters['threshold'])
            enable_integrin = bool(parameters['enable_integrin'])

            enable_complex = True
            if 'enable_complex' in parameters:
                enable_complex = bool(parameters['enable_complex'])

            clusters = None
            if 'clusters' in parameters and parameters['clusters']:
                clusters = list(parameters['clusters'])

            result_interactions, result_interactions_extended = extensions.cellphonedb_flask.cellphonedb.query.cluster_receptor_ligand_interactions(
                cells_to_clusters_result, threshold, enable_integrin, enable_complex, clusters)

            self._attach_csv(result_interactions.to_csv(index=False), 'result_interactions.csv')
            self._attach_csv(result_interactions_extended.to_csv(index=False),
                             'result_interactions_extended.txt')
            self._attach_csv(cells_to_clusters_result.to_csv(), 'cluster_counts.csv')

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
