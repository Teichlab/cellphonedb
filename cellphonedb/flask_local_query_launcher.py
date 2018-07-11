from cellphonedb.app_logger import app_logger
from cellphonedb.extensions import cellphonedb_flask


class FlaskLocalQueryLauncher:
    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            app_logger.info('Launching Query {}'.format(name))

        return method

    @staticmethod
    def search_interactions(input: str) -> None:
        cellphonedb_flask.cellphonedb.query.search_interactions(input)
