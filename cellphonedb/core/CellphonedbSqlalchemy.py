from cellphonedb.core.Cellphonedb import Cellphonedb
from cellphonedb.database.Database import Database
from cellphonedb.database.DatabaseManager import DatabaseManager

from sqlalchemy import create_engine

from cellphonedb.core.models import Base
from cellphonedb.core.repository.ComplexRepository import ComplexRepository
from cellphonedb.core.repository.InteractionRepository import InteractionRepository
from cellphonedb.core.repository.MultidataRepository import MultidataRepository
from cellphonedb.core.repository.ProteinRepository import ProteinRepository
from cellphonedb.core.repository.GeneRepository import GeneRepository


class CellphonedbSqlalchemy(Cellphonedb):
    def __init__(self, config):
        engine = create_engine(config['sqlalchemy']['uri'], echo=config['sqlalchemy']['echo'])
        database = Database(engine)
        database.base_model = Base
        database_manager = DatabaseManager(None, database)
        # TODO: Auto-load repositories
        database_manager.add_repository(ComplexRepository)
        database_manager.add_repository(GeneRepository)
        database_manager.add_repository(InteractionRepository)
        database_manager.add_repository(MultidataRepository)
        database_manager.add_repository(ProteinRepository)
        Cellphonedb.__init__(self, database_manager)
