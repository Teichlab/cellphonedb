from cellcommdb.extensions import db
from cellcommdb.models import Protein
import pandas as pd
import inspect


class Exporter(object):
    def __init__(self, app):
        self.app = app

    def protein(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            proteins = db.session.query(Protein)
            df = pd.read_sql(proteins.statement, db.engine)
            df.to_csv('out/%s' % output_name, index=False)
