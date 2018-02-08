from cellphonedb.database import DatabaseManager
from cellphonedb.queries import cells_to_clusters


class Cellphonedb(object):
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def cells_to_clusters(self, counts, meta):
        return cells_to_clusters.call(counts, meta)
