import pandas as pd

from cellcommdb.repository import multidata_repository


def expand_interactions_multidatas(interactions: pd.DataFrame, suffixes: list = ['_1', '_2']) -> pd.DataFrame:
    multidatas = multidata_repository.get_all_expanded()

    interactions_expanded = pd.merge(interactions, multidatas, left_on='multidata_1_id', right_on='id_multidata')
    interactions_expanded = pd.merge(interactions_expanded, multidatas, left_on='multidata_2_id',
                                     right_on='id_multidata', suffixes=suffixes)

    interactions_expanded.drop_duplicates(inplace=True)
    return interactions_expanded
