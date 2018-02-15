import json

from flask import request, Response

from cellphonedb import extensions
from cellphonedb.api_endpoints.endpoint_base import EndpointBase

from cellphonedb.common.generic_exception import GenericException


# curl -i \
#      --data "{\"receptor\": \"P25106\"}" \
#      http://127.0.0.1:5000/api/get_ligands_from_receptor
class GetRlLrInteractions(EndpointBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        receptor = parameters['receptor']

        try:
            result = extensions.cellphonedb_flask.cellphonedb.query.get_rl_lr_interactions_from_multidata(receptor, 0.3)

            if result.empty:
                self.attach_error(
                    {'code': 'result_not_found', 'title': '%s not found' % receptor,
                     'details': '%s is not in Cellphone Database' % receptor})
            else:
                self._attach_table(result.to_csv(index=False, sep='\t'), 'ligands')
        except GenericException as e:
            self.attach_error(e.args[0])

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
