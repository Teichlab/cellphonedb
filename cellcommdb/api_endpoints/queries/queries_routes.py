from cellcommdb.api_endpoints.queries.cell_to_cluster import CellToCluster
from cellcommdb.api_endpoints.queries.receptor_ligands_interactions import ReceptorLigandsInteractions


def add(api):
    api.add_resource(CellToCluster, '/cell_to_cluster')
    api.add_resource(ReceptorLigandsInteractions, '/receptor_ligands_interactions')
