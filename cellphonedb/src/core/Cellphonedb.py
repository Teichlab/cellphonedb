import os

from cellphonedb.src.core.collectors.collector import Collector
from cellphonedb.src.core.exporters.exporterlauncher import ExporterLauncher
from cellphonedb.src.core.methods.method_launcher import MethodLauncher
from cellphonedb.src.core.database import DatabaseManager
from cellphonedb.src.core.queries.query_launcher import QueryLauncher

cellphone_core_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = '{}/data'.format(cellphone_core_dir)

data_test_dir = '{}/tests/fixtures'.format(cellphone_core_dir)


class Cellphonedb(object):
    def __init__(self, database_manager: DatabaseManager, config):
        self.config = {'default_threads': config['threads']}
        self.database_manager = database_manager
        self.export = ExporterLauncher(self.database_manager)
        self.collect = Collector(self.database_manager)
        self.method = MethodLauncher(self.database_manager, self.config['default_threads'])
        self.query = QueryLauncher(self.database_manager)
        self.debug_mode = config['debug']
