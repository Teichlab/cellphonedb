from cellphonedb.api_endpoints.queries.cell_to_cluster import CellToCluster
from cellphonedb.api_endpoints.queries.get_rl_lr_interactions import GetRlLrInteractions
from cellphonedb.api_endpoints.queries.receptor_ligands_interactions import ReceptorLigandsInteractions


def add(api):
    api.add_resource(CellToCluster, '/cell_to_cluster')
    api.add_resource(ReceptorLigandsInteractions, '/receptor_ligands_interactions')
    api.add_resource(GetRlLrInteractions, '/get_ligands_from_receptor')
