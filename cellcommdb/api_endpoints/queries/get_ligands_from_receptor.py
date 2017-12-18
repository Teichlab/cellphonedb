import json

from flask import request, Response

from cellcommdb.api_endpoints.queries.query_base import QueryBase
from cellcommdb.queries import get_ligands_from_receptor


# curl -i \
#      -F parameters="{\"receptor\": \"P25106\"}" \
#      http://127.0.0.1:5000/api/get_ligands_from_receptor
class GetLigandsFromReceptor(QueryBase):
    def post(self):
        parameters = json.loads(request.form['parameters'])

        receptor = parameters['receptor']

        ligands = get_ligands_from_receptor.call(receptor, 0.3)

        self._attach_table(ligands.to_csv(index=False, sep='\t'), 'ligands')

        self._attach_json(self._status, at_first=True)
        self._commit_attachments()
        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
