from flask_restful import Api

from src.api_endpoints.web_api.method_web_api_endpoints import method_web_api_routes
from src.api_endpoints.web_api.query_web_api_endpoints import query_web_api_routes


def add(api: Api, prefix=''):
    method_web_api_routes.add(api, prefix=prefix + '/method')
    query_web_api_routes.add(api, prefix=prefix + '/query')
