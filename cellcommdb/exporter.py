from sqlalchemy import or_, and_

from cellcommdb.extensions import db
from cellcommdb.models import Protein, Multidata, Complex, ComplexComposition, Interaction, Gene
import pandas as pd
import inspect

from cellcommdb.tools import filters, database
from cellcommdb.unblend import Unblend
from utilities import dataframe_format


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

            proteins_multidata.rename(index=str, columns={'name': 'uniprot'}, inplace=True)

            proteins_multidata = dataframe_format.bring_columns_to_start(['uniprot'], proteins_multidata)
            proteins_multidata = dataframe_format.bring_columns_to_end(['tags', 'tags_reason'], proteins_multidata)
            proteins_multidata.to_csv('out/%s' % output_name, index=False)

    def complex(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            complex_query = db.session.query(Complex)
            multidata_query = db.session.query(Multidata)
            complex_composition_query = db.session.query(ComplexComposition)
            protein_query = db.session.query(Protein, Multidata).join(Multidata)

            complex_df = pd.read_sql(complex_query.statement, db.engine)
            multidata_df = pd.read_sql(multidata_query.statement, db.engine)
            complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)
            protein_df = pd.read_sql(protein_query.statement, db.engine)

            complex_complete = pd.merge(complex_df, multidata_df, left_on='complex_multidata_id', right_on='id')

            composition = []
            for complex_index, complex in complex_df.iterrows():
                complex_complex_composition = complex_composition_df[
                    complex_composition_df['complex_multidata_id'] == complex['complex_multidata_id']]

                protein_index = 1
                complex_proteins = {'complex_multidata_id': complex['complex_multidata_id'],
                                    'protein_1': None, 'protein_1_gene_name': None,
                                    'protein_2': None, 'protein_2_gene_name': None,
                                    'protein_3': None, 'protein_3_gene_name': None,
                                    'protein_4': None, 'protein_4_gene_name': None
                                    }
                for index, complex_composition in complex_complex_composition.iterrows():
                    proteine_name = \
                        multidata_df[multidata_df['id'] == complex_composition['protein_multidata_id']]['name'].values[
                            0]
                    complex_proteins['protein_%i' % protein_index] = proteine_name

                    entry_name = protein_df[protein_df['name'] == proteine_name]['entry_name'].values[0]
                    complex_proteins['protein_%i_gene_name' % protein_index] = entry_name
                    protein_index += 1

                composition.append(complex_proteins)

            complex_complete = pd.merge(complex_complete, pd.DataFrame(composition), on='complex_multidata_id')
            complex_complete.drop(['id_x', 'id_y', 'complex_multidata_id'], axis=1, inplace=True)

            # Edit order of the columns
            protein_headers = []

            for i in range(4):
                protein_headers.append('protein_%s' % (i + 1))
                protein_headers.append('protein_%s_gene_name' % (i + 1))

            complex_complete = dataframe_format.bring_columns_to_start(['name'] + protein_headers, complex_complete)
            complex_complete = dataframe_format.bring_columns_to_end(
                ['pdb_structure', 'pdb_id', 'stoichiometry', 'comments'], complex_complete)

            complex_complete.to_csv('out/%s' % output_name, index=False)

    def gene(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            gene_query = db.session.query(Gene, Multidata.name).join(Protein).join(Multidata)
            gene_df = pd.read_sql(gene_query.statement, db.engine)

            filters.remove_not_defined_columns(gene_df, database.get_column_table_names(Gene, db) + ['name'])

            gene_df.drop(['id', 'protein_id'], axis=1, inplace=True)

            gene_df.rename(index=str, columns={'name': 'uniprot'}, inplace=True)

            gene_df.to_csv('out/%s' % output_name, index=False)

    def interaction(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            interaction_query = db.session.query(Interaction)
            interaction_df = pd.read_sql(interaction_query.statement, db.engine)

            protein_query = db.session.query(Multidata.name, Protein.entry_name).join(Protein)
            protein_df = pd.read_sql(protein_query.statement, db.engine)

            interaction_df = Unblend.multidata(interaction_df, ['multidata_1_id', 'multidata_2_id'], 'multidata_name',
                                               True)

            interaction_df = pd.merge(interaction_df, protein_df, left_on=['multidata_name_1'], right_on=['name'],
                                      how='left')
            interaction_df.rename(index=str, columns={'entry_name': 'entry_name_1'}, inplace=True)

            interaction_df = pd.merge(interaction_df, protein_df, left_on=['multidata_name_2'], right_on=['name'],
                                      how='left')
            interaction_df.rename(index=str, columns={'entry_name': 'entry_name_2'}, inplace=True)

            filters.remove_not_defined_columns(interaction_df, ['multidata_name_1', 'multidata_name_2', 'entry_name_1',
                                                                'entry_name_2'] + database.get_column_table_names(
                Interaction, db))
            interaction_df.drop('id', axis=1, inplace=True)

            interaction_df = dataframe_format.bring_columns_to_start(
                ['multidata_name_1', 'entry_name_1', 'multidata_name_2',
                 'entry_name_2'], interaction_df)

            interaction_df.sort_values('source', ascending=False).to_csv('out/%s' % output_name, index=False)
