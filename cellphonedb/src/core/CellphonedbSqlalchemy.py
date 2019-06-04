import os

from sqlalchemy import create_engine

from cellphonedb.src.core.Cellphonedb import Cellphonedb
from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.database.Database import Database
from cellphonedb.src.core.database.DatabaseManager import DatabaseManager
from cellphonedb.src.core.database.sqlalchemy_models import Base
from cellphonedb.src.core.database.sqlalchemy_repository.ComplexRepository import ComplexRepository
from cellphonedb.src.core.database.sqlalchemy_repository.GeneRepository import GeneRepository
from cellphonedb.src.core.database.sqlalchemy_repository.InteractionRepository import InteractionRepository
from cellphonedb.src.core.database.sqlalchemy_repository.MultidataRepository import MultidataRepository
from cellphonedb.src.core.database.sqlalchemy_repository.ProteinRepository import ProteinRepository


class CellphonedbSqlalchemy(Cellphonedb):
    def __init__(self, config: dict, database_file=None, collecting=False):
        core_logger.setLevel(config['logger']['level'])
        core_logger.info('Initializing SqlAlchemy CellPhoneDB Core')

        if database_file:
            if not collecting and not os.path.exists(database_file):
                raise Exception('Given database file {} does not exist'.format(database_file))

            uri = self._build_sqlite_uri(database_file)
        else:
            # todo: Improve config stuff
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
    def _build_sqlite_uri(database_file):
        path = os.path.realpath(os.path.expanduser(database_file))
        core_logger.info('Using custom database at {}'.format(path))

        return 'sqlite:///{}'.format(path)

    @staticmethod
    def _build_uri(config):
        if config['sqlalchemy']['db_core']:

            file_path = os.path.dirname(os.path.realpath(__file__))

            if not config['sqlalchemy']['uri']:
                return 'sqlite:///{}/cellphone.db'.format(file_path)

            return 'sqlite:///{}/{}'.format(file_path, config['sqlalchemy']['uri'])
        else:
            return config['sqlalchemy']['uri']
