from cellphonedb.api_endpoints.web_api.query_web_api_endpoints.web_endpoint_query_search_interactions import \
    WebEndpointQuerySearchInteractions


def add(api, prefix=''):
    api.add_resource(WebEndpointQuerySearchInteractions, '{}/search_interactions'.format(prefix))
