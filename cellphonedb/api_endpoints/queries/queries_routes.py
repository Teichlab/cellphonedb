from cellphonedb.api_endpoints.queries.web_endpoint_cluster_statistical_analysis import \
    WebEndpointClusterStatisticalAnalysis
from cellphonedb.api_endpoints.queries.cell_to_cluster import CellToCluster
from cellphonedb.api_endpoints.queries.get_rl_lr_interactions import GetRlLrInteractions
from cellphonedb.api_endpoints.queries.cluster_receptor_ligand_interactions import ReceptorLigandInteractions
from cellphonedb.api_endpoints.queries.cluster_receptor_ligand_interactions_unprocessed import \
    ClusterReceptorLigandInteractionsUnprocessed


def add(api):
    api.add_resource(CellToCluster, '/cell_to_cluster')
    api.add_resource(ReceptorLigandInteractions, '/cluster_receptor_ligand_interactions')
    api.add_resource(ClusterReceptorLigandInteractionsUnprocessed, '/cluster_receptor_ligand_interactions_unprocessed')
    api.add_resource(GetRlLrInteractions, '/get_ligands_from_receptor')
    api.add_resource(WebEndpointClusterStatisticalAnalysis, '/cluster_statistical_analysis')
