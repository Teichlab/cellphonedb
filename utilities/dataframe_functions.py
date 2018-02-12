import pandas as pd

from utilities import dataframe_format


def dataframes_has_same_data(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame,
                             sort_column=None) -> pd.DataFrame:
    dataframe1 = dataframe1.copy(deep=True)
    dataframe2 = dataframe2.copy(deep=True)

    columns_names = list(dataframe1.columns.values)
    columns_names.sort()
    dataframe1 = dataframe_format.bring_columns_to_end(columns_names, dataframe1)

    columns_names = list(dataframe2.columns.values)
    columns_names.sort()
    dataframe2 = dataframe_format.bring_columns_to_end(columns_names, dataframe2)

    if sort_column:
        dataframe1 = dataframe1.sort_values(sort_column).reset_index(drop=True)
        dataframe2 = dataframe2.sort_values(sort_column).reset_index(drop=True)

    dataframe1.to_csv('TEST_dataframe1.csv', index=False)
    dataframe2.to_csv('TEST_dataframe2.csv', index=False)

    return dataframe1.equals(dataframe2)
