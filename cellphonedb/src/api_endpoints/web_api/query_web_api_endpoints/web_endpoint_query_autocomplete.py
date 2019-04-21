import json
import sys
import traceback

import flask
from flask import request

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase


class WebEndpointQueryAutocomplete(WebApiEndpointBase):
    def post(self):
        parameters = json.loads(request.get_data(as_text=True))

        partial_element = parameters['partial_element']

        if len(partial_element) < 2:
            return flask.jsonify({'success': True, 'result': []})

        try:
            interactions = cellphonedb_app.cellphonedb.query.autocomplete_launcher(partial_element)
            response = {
                'success': True,
                'result': interactions.to_dict(orient='records')
            }
        except:
            response = {
                'success': False
            }
            print(traceback.print_exc(file=sys.stdout))

        return flask.jsonify(response)
