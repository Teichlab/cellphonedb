import pandas as pd

from cellcommdb.repository import multidata_repository


def expand_interactions_multidatas(interactions: pd.DataFrame, suffixes: list = ['_1', '_2']) -> pd.DataFrame:
    multidatas = multidata_repository.get_all_expanded()

    interactions_expanded = pd.merge(interactions, multidatas, left_on='multidata_1_id', right_on='id_multidata')
    interactions_expanded = pd.merge(interactions_expanded, multidatas, left_on='multidata_2_id',
                                     right_on='id_multidata', suffixes=suffixes)

    interactions_expanded.drop_duplicates(inplace=True)
    return interactions_expanded


def get_duplicated(interactions: pd.DataFrame, column_1: str, column_2: str) -> pd.DataFrame:
    def duplicated(row):
        if len(interactions[(row[column_1] == interactions[column_1]) & (
                row[column_2] == interactions[column_2])]) > 1:
            return True

        if (row[column_1] != row[column_2]) & len(
                interactions[(row[column_1] == interactions[column_2]) & (
                        row[column_2] == interactions[column_1])]) > 0:
            return True
        return False

    result = interactions[interactions.apply(duplicated, axis=1)]

    return result
