import pandas as pd
from sqlalchemy import or_

from cellcommdb.extensions import db
from cellcommdb.models import Interaction


def get_interactions_by_multidata_id(id):
    query = db.session.query(Interaction).filter(
        or_(Interaction.multidata_1_id == id, Interaction.multidata_2_id == id))
    result = pd.read_sql(query.statement, db.engine)

    return result
