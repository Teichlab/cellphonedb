from cellphonedb.core.Cellphonedb import Cellphonedb
from cellphonedb.database.Database import Database
from cellphonedb.database.DatabaseManager import DatabaseManager

from sqlalchemy import create_engine

from cellphonedb.repository.ComplexRepository import ComplexRepository
from cellphonedb.repository.InteractionRepository import InteractionRepository
from cellphonedb.repository.MultidataRepository import MultidataRepository
from cellphonedb.repository.ProteinRepository import ProteinRepository
from cellphonedb.repository.GeneRepository import GeneRepository


class CellphonedbSqlalchemy(Cellphonedb):
    def __init__(self):
        # TODO: Hardcoded. Move to config file
        engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/cellphonedb', echo=True)
        # engine = create_engine('sqlite:///:memory:', echo=True)
        database = Database(engine)
        database_manager = DatabaseManager(None, database)
        # TODO: Auto-load repositories
        database_manager.add_repository(ComplexRepository)
        database_manager.add_repository(GeneRepository)
        database_manager.add_repository(InteractionRepository)
        database_manager.add_repository(MultidataRepository)
        database_manager.add_repository(ProteinRepository)
        Cellphonedb.__init__(self, database_manager)
