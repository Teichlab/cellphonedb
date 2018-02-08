from cellphonedb.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy


class CellphonedbFlask(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.cellphonedb = CellphonedbSqlalchemy()
