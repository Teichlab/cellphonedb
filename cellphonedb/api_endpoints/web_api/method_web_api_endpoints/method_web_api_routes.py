from cellphonedb.api_endpoints.web_api.method_web_api_endpoints.web_endpoint_cluster_statistical_analysis import \
    WebEndpointClusterStatisticalAnalysis


def add(api, prefix=''):
    api.add_resource(WebEndpointClusterStatisticalAnalysis, '{}/cluster_statistical_analysis'.format(prefix))
