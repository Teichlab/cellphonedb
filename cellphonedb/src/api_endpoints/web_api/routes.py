import flask
from flask_restful import Api

from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints import query_web_api_routes
from cellphonedb.src.api_endpoints.web_api.web_api_endpoint_base import WebApiEndpointBase
from cellphonedb.src.database.manager import DatabaseVersionManager


class DatabaseVersionsEndpoint(WebApiEndpointBase):
    def get(self):
        response = DatabaseVersionManager.list_local_versions()

        return flask.jsonify(response)


def add(api: Api, prefix=''):
    query_web_api_routes.add(api, prefix=prefix + '/query')
    api.add_resource(DatabaseVersionsEndpoint, '{}/database_versions'.format(prefix))
