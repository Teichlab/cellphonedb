import json

from flask import request, Response

from cellcommdb.api_endpoints.endpoint_base import EndpointBase
from cellcommdb.queries import get_ligands_from_receptor

# curl -i \
#      --data "{\"receptor\": \"P25106\"}" \
#      http://127.0.0.1:5000/api/get_ligands_from_receptor
from cellcommdb.common.generic_exception import GenericException
from cellcommdb.repository import multidata_repository


class GetLigandsFromReceptor(EndpointBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        receptor = parameters['receptor']

        multidata_receptor = multidata_repository.get_multidata_from_string(receptor)

        if multidata_receptor.empty:
            self.attach_error(
                {'code': 'result_not_found', 'title': '%s not found' % receptor,
                 'details': '%s is not in Cellphone Database' % receptor})

        if not self._errors:
            try:
                ligands = get_ligands_from_receptor.call(multidata_receptor.iloc[0], 0.3)
                self._attach_table(ligands.to_csv(index=False, sep='\t'), 'ligands')
            except GenericException as e:
                self.attach_error(e.args[0])

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
