import pandas as pd

from cellphonedb.utils import dataframe_format


def dataframes_has_same_data(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame,
                             round_decimals: bool = False) -> pd.DataFrame:
    dataframe1 = dataframe1.copy(deep=True)
    dataframe2 = dataframe2.copy(deep=True)

    columns_names_1 = list(dataframe1.columns.values)
    columns_names_1.sort()

    dataframe1 = dataframe_format.bring_columns_to_end(columns_names_1, dataframe1)

    columns_names_2 = list(dataframe2.columns.values)
    columns_names_2.sort()
    dataframe2 = dataframe_format.bring_columns_to_end(columns_names_2, dataframe2)

    if not dataframe1.empty:
        dataframe1 = dataframe1.sort_values(columns_names_1).reset_index(drop=True)

        if round_decimals:
            dataframe1 = dataframe1.round(5)

    if not dataframe2.empty:
        dataframe2 = dataframe2.sort_values(columns_names_2).reset_index(drop=True)

        if round_decimals:
            dataframe2 = dataframe2.round(5)

    if dataframe1.empty and dataframe2.empty:
        return pd.Series(dataframe1.columns.values).equals(pd.Series(dataframe2.columns.values))

    return dataframe1.equals(dataframe2)
