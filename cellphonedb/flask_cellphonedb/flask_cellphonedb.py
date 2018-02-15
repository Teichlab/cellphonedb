from cellphonedb.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy


class CellphonedbFlask(object):
    def __init__(self, app=None, config=None):
        self.app = app
        if app is not None:
            self.init_app(config)

    def init_app(self, config):
        self.cellphonedb = CellphonedbSqlalchemy(config)
