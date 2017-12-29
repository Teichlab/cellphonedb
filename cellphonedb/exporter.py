from cellphonedb.exporters import ligands_receptors_proteins_exporter, complex_exporter
from cellphonedb.extensions import db
import pandas as pd
import inspect

from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.interaction.db_model_interaction import Interaction
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein
from cellphonedb.tools import filters, database
from cellphonedb.unblend import Unblend
from utilities import dataframe_format


class Exporter(object):
    def __init__(self, app):
        self.app = app

    def all(self):
        self.protein()
        complex(self.app)
        self.gene()
        self.interaction()

    def ligands_receptors_proteins(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        result = ligands_receptors_proteins_exporter.call()
        result.to_csv('out/%s' % output_name, index=False)

    def complex(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        result = complex_exporter.call()
        result.to_csv('out/%s' % output_name, index=False)


    def protein(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            proteins_query = db.session.query(Protein)
            multidata_query = db.session.query(Multidata)

            proteins_df = pd.read_sql(proteins_query.statement, db.engine)
            multidata_df = pd.read_sql(multidata_query.statement, db.engine)

            proteins_multidata = pd.merge(proteins_df, multidata_df, left_on='protein_multidata_id',
                                          right_on='id_multidata')

            proteins_multidata.drop(['id_multidata', 'id_protein', 'protein_multidata_id'], axis=1, inplace=True)

            proteins_multidata.rename(index=str, columns={'name': 'uniprot'}, inplace=True)

            proteins_multidata = dataframe_format.bring_columns_to_start(['uniprot'], proteins_multidata)
            proteins_multidata = dataframe_format.bring_columns_to_end(['tags', 'tags_reason'], proteins_multidata)
            proteins_multidata.to_csv('out/%s' % output_name, index=False)

    def gene(self, output_name=None):
        if not output_name:
            current_method_name = inspect.getframeinfo(inspect.currentframe()).function
            output_name = '%s.csv' % current_method_name

        with self.app.app_context():
            gene_query = db.session.query(Gene, Multidata.name).join(Protein).join(Multidata)
            gene_df = pd.read_sql(gene_query.statement, db.engine)

            filters.remove_not_defined_columns(gene_df, database.get_column_table_names(Gene, db) + ['name'])

            gene_df.drop(['id_gene', 'protein_id'], axis=1, inplace=True)

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
            interaction_df.drop('id_interaction', axis=1, inplace=True)

            interaction_df = dataframe_format.bring_columns_to_start(
                ['multidata_name_1', 'entry_name_1', 'multidata_name_2',
                 'entry_name_2'], interaction_df)

            interaction_df.sort_values('source', ascending=False).to_csv('out/%s' % output_name, index=False)
