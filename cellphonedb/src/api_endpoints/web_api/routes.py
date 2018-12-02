from flask_restful import Api

from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints import query_web_api_routes


def add(api: Api, prefix=''):
    query_web_api_routes.add(api, prefix=prefix + '/query')
