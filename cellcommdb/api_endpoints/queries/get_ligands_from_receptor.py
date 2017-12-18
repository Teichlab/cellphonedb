import json

from flask import request, Response

from cellcommdb.api_endpoints.queries.query_base import QueryBase
from cellcommdb.queries import get_ligands_from_receptor

# curl -i \
#      --data "{\"receptor\": \"P25106\"}" \
#      http://127.0.0.1:5000/api/get_ligands_from_receptor
from cellcommdb.common.generic_exception import GenericException


class GetLigandsFromReceptor(QueryBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        receptor = parameters['receptor']

        try:
            ligands = get_ligands_from_receptor.call(receptor, 0.3)
            self._attach_table(ligands.to_csv(index=False, sep='\t'), 'ligands')
        except GenericException as e:
            self._attach_error(e.args[0])

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
