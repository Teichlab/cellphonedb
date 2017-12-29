import pandas as pd

from cellphonedb.extensions import db
from cellphonedb.models.interaction.db_model_interaction import Interaction
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein
from cellphonedb.tools import filters, database
from cellphonedb.unblend import Unblend
from utilities import dataframe_format


def call():
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

    return interaction_df
