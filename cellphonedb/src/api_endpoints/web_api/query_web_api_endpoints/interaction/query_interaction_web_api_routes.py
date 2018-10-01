from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.interaction.web_endpoint_query_interaction_gene import \
    WebEndpointQueryInteractionGene


def add(api, prefix=''):
    api.add_resource(WebEndpointQueryInteractionGene, '{}/gene'.format(prefix))
