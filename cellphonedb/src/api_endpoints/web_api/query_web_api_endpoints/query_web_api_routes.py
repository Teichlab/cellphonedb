from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.complex import query_complex_web_api_routes
from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.interaction import query_interaction_web_api_routes
from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.web_endpoint_query_autocomplete import \
    WebEndpointQueryAutocomplete
from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.web_endpoint_query_database import \
    WebEndpointQueryDatabase
from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.web_endpoint_query_find_interactions_by_element import \
    WebEndpointQueryFindInteractionsByElement


def add(api, prefix=''):
    query_interaction_web_api_routes.add(api, '{}/interaction'.format(prefix))
    query_complex_web_api_routes.add(api, '{}/complex'.format(prefix))

    api.add_resource(WebEndpointQueryFindInteractionsByElement, '{}/find_interactions_by_element'.format(prefix))
    api.add_resource(WebEndpointQueryAutocomplete, '{}/autocomplete'.format(prefix))
    api.add_resource(WebEndpointQueryDatabase, '{}/database_versions'.format(prefix))
