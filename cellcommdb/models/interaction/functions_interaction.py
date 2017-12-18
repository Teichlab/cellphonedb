import pandas as pd

from cellcommdb.repository import multidata


def expand_interactions_multidatas(interactions, suffixes=['_1', '_2']):
    """

    :type interactions: pd.DataFrame
    :type suffixes: list
    :rtype: pd.DataFrame
    """

    multidatas = multidata.get_all_expanded()

    interactions_expanded = pd.merge(interactions, multidatas, left_on='multidata_1_id', right_on='id_multidata')
    interactions_expanded = pd.merge(interactions_expanded, multidatas, left_on='multidata_2_id',
                                     right_on='id_multidata', suffixes=suffixes)

    return interactions_expanded
