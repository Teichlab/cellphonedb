from cellcommdb.extensions import db
from cellcommdb.models import Protein, Multidata, Complex, Complex_composition
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

    def complex(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            complex_query = db.session.query(Complex)
            multidata_query = db.session.query(Multidata)
            complex_composition_query = db.session.query(Complex_composition)


            complex_df = pd.read_sql(complex_query.statement, db.engine)
            multidata_df = pd.read_sql(multidata_query.statement, db.engine)
            complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)

            complex_complete = pd.merge(complex_df, multidata_df, left_on='complex_multidata_id', right_on='id')


            composition = []
            for complex_index, complex in complex_df.iterrows():
                complex_complex_composition = complex_composition_df[
                    complex_composition_df['complex_multidata_id'] == complex['complex_multidata_id']]

                protein_index = 1
                complex_proteins = {'complex_multidata_id': complex['complex_multidata_id'], 'protein_1': None,
                                    'protein_2': None, 'protein_3': None, 'protein_4': None}
                for index, complex_composition in complex_complex_composition.iterrows():
                    proteine_name = multidata_df.iloc[complex_composition['protein_multidata_id'], :]['name']
                    complex_proteins['protein_%i' % protein_index] = proteine_name
                    protein_index += 1

                composition.append(complex_proteins)

            complex_complete = pd.merge(complex_complete, pd.DataFrame(composition), on='complex_multidata_id')
            complex_complete.to_csv('out/%s' % output_name, index=False)
