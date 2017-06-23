from sqlalchemy import or_, and_

from cellcommdb.extensions import db
from cellcommdb.models import Protein, Multidata, Complex, Complex_composition, Interaction, Gene
import pandas as pd
import inspect

from cellcommdb.tools import filters


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

            proteins_multidata.drop(['id_x', 'id_y', 'protein_multidata_id'], axis=1, inplace=True)

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
            complex_complete.drop(['id_x', 'id_y', 'complex_multidata_id'], axis=1, inplace=True)
            complex_complete.to_csv('out/%s' % output_name, index=False)

    def interaction(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        multidata_query = db.session.query(Multidata)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)

        interaction_query = db.session.query(Interaction)
        interaction_df = pd.read_sql(interaction_query.statement, db.engine)

        # csv_interaction_df = pd.merge(interaction_df, multidata_df, left_on='unityinteraction_multidata_1_id',
        #                               right_on='id')
        # csv_interaction_df.rename(index=str, columns={'name': 'uniprot_1'}, inplace=True)
        # csv_interaction_df = pd.merge(csv_interaction_df, multidata_df, left_on='unityinteraction_multidata_2_id',
        #                               right_on='id')
        # csv_interaction_df.rename(index=str, columns={'name': 'uniprot_2'}, inplace=True)
        # csv_interaction_df = filters.remove_not_defined_columns(csv_interaction_df,
        #                                                         ['uniprot_1', 'uniprot_2', 'score_1', 'score_2'])

        complex_query = db.session.query(Complex)
        complex_df = pd.read_sql(complex_query.statement, db.engine)

        complex_ids = complex_df['complex_multidata_id'].tolist()

        complex_composition_query = db.session.query(Complex_composition)
        complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)

        print complex_ids
        for interaction_index, interaction in interaction_df.iterrows():
            if interaction['unityinteraction_multidata_1_id'] in complex_ids:
                print int(interaction['unityinteraction_multidata_1_id'])
                print complex_composition_df[
                    complex_composition_df['complex_multidata_id'] == interaction['unityinteraction_multidata_1_id']]

            if interaction['unityinteraction_multidata_2_id'] in complex_ids:
                print int(interaction['unityinteraction_multidata_2_id'])
                print complex_composition_df[
                    complex_composition_df['complex_multidata_id'] == interaction['unityinteraction_multidata_2_id']]

                # csv_interaction_df.to_csv('out/%s' % output_name, index=False)

    def gene(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            gene_query = db.session.query(Gene)
            proteins_query = db.session.query(Protein)
            multidata_query = db.session.query(Multidata)

            gene_df = pd.read_sql(gene_query.statement, db.engine)
            proteins_df = pd.read_sql(proteins_query.statement, db.engine)
            multidata_df = pd.read_sql(multidata_query.statement, db.engine)

            gene_df.rename(index=str, columns={'name': 'gene_table_name'}, inplace=True)
            gene_protein = pd.merge(gene_df, proteins_df, left_on='protein_id', right_on='id')
            gene_protein_multidata = pd.merge(gene_protein, multidata_df, left_on='protein_multidata_id', right_on='id')

            gene_protein_multidata.drop(['id', 'id_x', 'id_y', 'protein_multidata_id', 'protein_id'], axis=1,
                                        inplace=True)

            gene_protein_multidata.to_csv('out/%s' % output_name, index=False)

    def protein_type_filtered(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        complex_composition_query = db.session.query(Complex_composition.protein_multidata_id)

        with self.app.app_context():
            proteins_query = db.session.query(Protein, Multidata).join(Multidata).filter(and_(
                or_(Protein.membrane_type == 'singlepass_typeI',
                    Protein.membrane_type == 'singlepass_typeII',
                    Protein.membrane_type == 'GPI-anchor'),
                ~Multidata.id.in_(complex_composition_query)
            ))

            proteins_df = pd.read_sql(proteins_query.statement, db.engine)
            proteins_df.drop('id', axis=1, inplace=True)

            proteins_df.to_csv('out/%s' % output_name, index=False)
