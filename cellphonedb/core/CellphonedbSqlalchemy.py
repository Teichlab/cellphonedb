from cellphonedb.core.Cellphonedb import Cellphonedb
from cellphonedb.database.Database import Database
from cellphonedb.database.DatabaseManager import DatabaseManager

from sqlalchemy import create_engine


class CellphonedbSqlalchemy(Cellphonedb):
    def __init__(self):
        # TODO: Hardcoded move to config file
        engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/cellphonedb', echo=True)
        # engine = create_engine('sqlite:///:memory:', echo=True)
        database = Database(engine)
        database_manager = DatabaseManager(None, database)
        Cellphonedb.__init__(self, database_manager)
