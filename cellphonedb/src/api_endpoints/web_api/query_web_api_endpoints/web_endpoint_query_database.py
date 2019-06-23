import flask
from cellphonedb.src.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase
from cellphonedb.src.database.manager import DatabaseVersionManager


class WebEndpointQueryDatabase(WebApiEndpointBase):
    def get(self):
        response = DatabaseVersionManager.list_local_versions()

        return flask.jsonify(response)
