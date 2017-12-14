import json

import pandas as pd
from flask import request, Response

from cellcommdb.api_endpoints.queries.query_base import QueryBase
from cellcommdb.queries import receptor_ligands_interactions


# curl -i \
#      -F "cell_to_clusters_file=@cellcommdb/data/queries/cells_to_clusters.csv;type=text/csv" \
#      -F parameters="{\"threshold\": 0.1}" \
#      http://127.0.0.1:5000/api/receptor_ligands_interactions


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
            self._attach_csv(result_interactions.to_csv(index=False), 'result_interactions.csv')
            self._attach_csv(result_interactions_extended.to_csv(index=False),
                             'result_interactions_extended.txt')

        self._attach_json(self._status, at_first=True)

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
