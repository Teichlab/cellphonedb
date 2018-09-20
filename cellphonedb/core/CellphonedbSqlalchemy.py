import os

from cellphonedb.core.Cellphonedb import Cellphonedb
from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.database.Database import Database
from cellphonedb.core.database.DatabaseManager import DatabaseManager

from sqlalchemy import create_engine

from cellphonedb.core.database.sqlalchemy_models import Base
from cellphonedb.core.database.sqlalchemy_repository.ComplexRepository import ComplexRepository
from cellphonedb.core.database.sqlalchemy_repository.InteractionRepository import InteractionRepository
from cellphonedb.core.database.sqlalchemy_repository.MultidataRepository import MultidataRepository
from cellphonedb.core.database.sqlalchemy_repository.ProteinRepository import ProteinRepository
from cellphonedb.core.database.sqlalchemy_repository.GeneRepository import GeneRepository


class CellphonedbSqlalchemy(Cellphonedb):
    def __init__(self, config: dict):
        core_logger.setLevel(config['logger']['level'])
        core_logger.info('Initializing SqlAlchemy CellPhoneDB Core')

        uri = self._build_uri(config)

        core_logger.debug('Database Uri: {}'.format(uri))

        engine = create_engine(uri)
        database = Database(engine)
        database.base_model = Base
        database_manager = DatabaseManager(None, database)
        # TODO: Auto-load repositories
        database_manager.add_repository(ComplexRepository)
        database_manager.add_repository(GeneRepository)
        database_manager.add_repository(InteractionRepository)
        database_manager.add_repository(MultidataRepository)
        database_manager.add_repository(ProteinRepository)
        Cellphonedb.__init__(self, database_manager, config)

    @staticmethod
    def _build_uri(config):
        if config['sqlalchemy']['db_core']:
            file_path = os.path.dirname(os.path.realpath(__file__))

            if not config['sqlalchemy']['uri']:
                return 'sqlite:///{}/cellphone.db'.format(file_path)

            return 'sqlite:///{}/{}'.format(file_path, config['sqlalchemy']['uri'])


        else:
            return config['sqlalchemy']['uri']
