import json

from flask import request, Response

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase


class WebEndpointQueryComplexDeconvoluted(WebApiEndpointBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        complex_name = parameters['complex_name']

        deconvoluted = cellphonedb_app.cellphonedb.query.get_complex_deconvoluted(complex_name)

        if deconvoluted.empty:
            self.attach_error(
                {'code': 'element_not_found', 'title': '%s is not CellPhoneDB Complex' % complex_name,
                 'details': '%s is not present in CellPhoneDB complex table' % complex_name})
        else:
            self._attach_csv(deconvoluted.to_csv(index=False, sep=','), 'result')

        self._commit_attachments()

        return Response(self._msg.as_string(), mimetype='multipart/form-data; boundary="%s"' % self._msg.get_boundary())
