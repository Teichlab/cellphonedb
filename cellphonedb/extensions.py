from flask_sqlalchemy import SQLAlchemy

from cellphonedb.flask_cellphonedb.flask_cellphonedb import CellphonedbFlask

db = SQLAlchemy()  # TODO: remove me
cellphonedb_flask = CellphonedbFlask()
