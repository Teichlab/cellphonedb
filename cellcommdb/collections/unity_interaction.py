import os

import pandas as pd

from cellcommdb.api import current_dir
from cellcommdb.blend import Blend
from cellcommdb.extensions import db
from cellcommdb.models import UnityInteraction
from cellcommdb.tools import filters, database


def load(unity_interaction_file=None):
    if not unity_interaction_file:
        unity_interaction_file = os.path.join(current_dir, 'data', 'unity_interaction.csv')

    csv_unity_interaction_df = pd.read_csv(unity_interaction_file)

    unity_interaction_df = Blend.blend_multidata(csv_unity_interaction_df, ['name'])

    unity_interaction_df.rename(index=str, columns={'id': 'multidata_id'}, inplace=True)

    filters.remove_not_defined_columns(unity_interaction_df, database.get_column_table_names(UnityInteraction, db))
    unity_interaction_df.to_sql(name='unity_interaction', if_exists='append', con=db.engine, index=False)
