from cellcommdb.extensions import db
from cellcommdb.models import Protein, Multidata
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
            proteins_query = db.session.query(Protein)
            multidata_query = db.session.query(Multidata)

            proteins_df = pd.read_sql(proteins_query.statement, db.engine)
            multidata_df = pd.read_sql(multidata_query.statement, db.engine)

            proteins_multidata = pd.merge(proteins_df, multidata_df, left_on='protein_multidata_id', right_on='id')

            proteins_multidata.to_csv('out/%s' % output_name, index=False)
