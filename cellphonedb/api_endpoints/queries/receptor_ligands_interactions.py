import json

import pandas as pd
from flask import request, Response

from cellphonedb import extensions
from cellphonedb.api_endpoints.endpoint_base import EndpointBase

# curl -i \
#      -F "cell_to_clusters_file=@cellphonedb/data/queries/cells_to_clusters.csv;type=text/csv" \
#      -F parameters="{\"threshold\": 0.1, \"enable_integrin\": \"true\"}" \
#      http://127.0.0.1:5000/api/receptor_ligands_interactions
#

class ReceptorLigandsInteractions(EndpointBase):
    def post(self):
        cells_to_clusters_file = self._read_table(request.files['cell_to_clusters_file'], True)

        if not isinstance(cells_to_clusters_file, pd.DataFrame):
            self.attach_error(
                {'code': 'parsing_error', 'title': 'Error parsing counts file', 'detail': 'Error parsing counts file'})

        if not self._errors:
            parameters = json.loads(request.form['parameters'])
            threshold = float(parameters['threshold'])
            enable_integrin = bool(parameters['enable_integrin'])
            enable_transmembrane = bool(parameters['enable_transmembrane'])
            enable_secreted = bool(parameters['enable_secreted'])
            enable_complex = True
            if 'enable_complex' in parameters:
                enable_complex = bool(parameters['enable_complex'])

            clusters = None
            if 'clusters' in parameters and parameters['clusters']:
                clusters = list(parameters['clusters'])

            result_interactions, result_interactions_extended = extensions.cellphonedb_flask.cellphonedb.query.receptor_ligands_interactions(
                cells_to_clusters_file, threshold, enable_integrin, enable_transmembrane, enable_secreted,
                enable_complex, clusters)
            self._attach_csv(result_interactions.to_csv(index=False), 'result_interactions.csv')
            self._attach_csv(result_interactions_extended.to_csv(index=False),
                             'result_interactions_extended.txt')

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
