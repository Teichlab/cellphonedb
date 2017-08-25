import os

import pandas as pd

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Multidata, UnityInteraction
from cellcommdb.tools import filters, database


def load(unity_interaction_file=None):
    if not unity_interaction_file:
        unity_interaction_file = os.path.join(current_dir, 'data', 'unity_interaction.csv')

    csv_unity_interaction_df = pd.read_csv(unity_interaction_file)
    csv_unity_interaction_df.drop('id', axis=1, inplace=True)

    multidata_query = db.session.query(Multidata)
    multidata_df = pd.read_sql(multidata_query.statement, db.engine)

    unity_interaction_df = pd.merge(multidata_df, csv_unity_interaction_df, on='name')


    unity_interaction_df.rename(index=str, columns={'id': 'multidata_id'}, inplace=True)

    filters.remove_not_defined_columns(unity_interaction_df, database.get_column_table_names(UnityInteraction, db))
    unity_interaction_df.to_sql(name='unity_interaction', if_exists='append', con=db.engine, index=False)
