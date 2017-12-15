import pandas as pd
from sqlalchemy import or_

from cellcommdb.extensions import db
from cellcommdb.models.interaction.db_model_interaction import Interaction
from cellcommdb.repository import multidata


def get_interactions_by_multidata_id(id):
    """

    :type id: int
    :rtype: pd.DataFrame
    """
    query = db.session.query(Interaction).filter(
        or_(Interaction.multidata_1_id == int(id), Interaction.multidata_2_id == int(id)))
    result = pd.read_sql(query.statement, db.engine)

    return result


def expand_interactions_multidatas(interactions, suffixes=['_1', '_2']):
    """

    :type interactions: pd.DataFrame
    :type suffixes: list
    :rtype: pd.DataFrame
    """

    multidatas = multidata.get_all()

    interactions_expanded = pd.merge(interactions, multidatas, left_on='multidata_1_id', right_on='id_multidata')
    interactions_expanded = pd.merge(interactions_expanded, multidatas, left_on='multidata_2_id',
                                     right_on='id_multidata', suffixes=suffixes)

    return interactions_expanded


def get_interactions_multidata_by_multidata_id(id):
    """

    :type id: int
    :rtype: pd.DataFrame
    """

    interactions = get_interactions_by_multidata_id(id)
    interactions_expanded = expand_interactions_multidatas(interactions)
    return interactions_expanded
