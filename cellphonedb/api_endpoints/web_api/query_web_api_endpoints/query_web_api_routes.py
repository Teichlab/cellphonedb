from cellphonedb.api_endpoints.web_api.query_web_api_endpoints.interaction import query_interaction_web_api_routes
from cellphonedb.api_endpoints.web_api.query_web_api_endpoints.web_endpoint_query_search_interactions import \
    WebEndpointQuerySearchInteractions


def add(api, prefix=''):
    query_interaction_web_api_routes.add(api, '{}/interaction'.format(prefix))
    api.add_resource(WebEndpointQuerySearchInteractions, '{}/search_interactions'.format(prefix))