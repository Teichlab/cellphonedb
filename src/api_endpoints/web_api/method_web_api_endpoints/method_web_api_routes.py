from src.api_endpoints.web_api.method_web_api_endpoints.web_endpoint_analysis import \
    WebEndpointAnalysis


def add(api, prefix=''):
    api.add_resource(WebEndpointAnalysis, '{}/analysis'.format(prefix))
