import os

import pandas as pd

from cellphonedb.api import current_dir
from cellphonedb.blend import Blend
from cellphonedb.extensions import db
from cellphonedb.models.interaction.db_model_interaction import Interaction
from cellphonedb.tools import filters, database


def load(interaction_file=None):
    if not interaction_file:
        interaction_file = os.path.join(current_dir, 'data', 'interaction.csv')

    csv_interaction_df = pd.read_csv(interaction_file, quotechar='"', na_values='NA', sep=',')

    interaction_df = Blend.blend_multidata(csv_interaction_df, ['multidata_name_1', 'multidata_name_2'])

    filters.remove_not_defined_columns(interaction_df, database.get_column_table_names(Interaction, db))

    interaction_df.to_sql(name='interaction', if_exists='append', con=db.engine, index=False)
