from cellphonedb.src.app import app_config
from cellphonedb.src.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy


def create_app(verbose: bool = None, database_file=None, collecting=False):
    config = app_config.AppConfig(verbose=verbose)
    cellphone_config = config.get_cellphone_core_config()
    return CellphonedbSqlalchemy(cellphone_config, database_file, collecting)
