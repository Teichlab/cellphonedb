import pandas as pd

from utils import dataframe_format


def dataframes_has_same_data(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame,
                             round_decimals: bool = False) -> pd.DataFrame:
    dataframe1 = dataframe1.copy(deep=True)
    dataframe2 = dataframe2.copy(deep=True)

    columns_names = list(dataframe1.columns.values)
    columns_names.sort()

    dataframe1 = dataframe_format.bring_columns_to_end(columns_names, dataframe1)

    columns_names = list(dataframe2.columns.values)
    columns_names.sort()
    dataframe2 = dataframe_format.bring_columns_to_end(columns_names, dataframe2)

    if not dataframe1.empty:
        dataframe1 = dataframe1.sort_values(columns_names).reset_index(drop=True)

        if round_decimals:
            dataframe1 = dataframe1.round(5)

    if not dataframe2.empty:
        dataframe2 = dataframe2.sort_values(columns_names).reset_index(drop=True)

        if round_decimals:
            dataframe2 = dataframe2.round(5)

    return dataframe1.equals(dataframe2)
