import pandas as pd

from cellphonedb.core.collectors.collector import Collector
from cellphonedb.core.exporters.exporterlauncher import ExporterLauncher
from cellphonedb.core.queries.querylauncher import QueryLauncher
from cellphonedb.database import DatabaseManager


class Cellphonedb(object):
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        self.export = ExporterLauncher(self.database_manager)
        self.collect = Collector(self.database_manager)
        self.query = QueryLauncher(self.database_manager)
