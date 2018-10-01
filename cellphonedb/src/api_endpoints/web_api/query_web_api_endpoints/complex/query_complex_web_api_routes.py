from cellphonedb.src.api_endpoints.web_api.query_web_api_endpoints.complex.web_endpoint_query_complex_deconvoluted import \
    WebEndpointQueryComplexDeconvoluted


def add(api, prefix=''):
    api.add_resource(WebEndpointQueryComplexDeconvoluted, '{}/deconvoluted'.format(prefix))
