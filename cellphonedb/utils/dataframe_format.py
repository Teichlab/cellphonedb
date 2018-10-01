import pandas as pd


def bring_columns_to_start(columns, dataframe):
    """

    :type columns: list
    :type dataframe: pd.DataFrame
    :rtype: pd.DataFrame
    """
    column_headers = list(dataframe.columns.values)
    for column in reversed(columns):
        column_headers.insert(0, column_headers.pop(column_headers.index(column)))

    result = dataframe[column_headers].copy()
    return result


def bring_columns_to_end(columns, dataframe):
    """

    :type columns: list
    :type dataframe: pd.DataFrame
    :rtype: pd.DataFrame
    """

    column_headers = list(dataframe.columns.values)
    for column in columns:
        column_headers.append(column_headers.pop(column_headers.index(column)))

    result = dataframe[column_headers].copy()
    return result


def change_column_suffix(dataframe: pd.DataFrame, old_suffix: str, new_suffix: str) -> pd.DataFrame:
    """
    Renames multiple columns suffixes
    """
    column_names = list(dataframe.columns.values)

    renamed_columns = {}
    for column_name in column_names:
        if column_name.endswith(old_suffix):
            new_name = column_name[:-len(old_suffix)] + new_suffix
            renamed_columns[column_name] = new_name
    interaction_preprocess_collector.py
    dataframe = dataframe.rename(index=str, columns=renamed_columns)
    return dataframe
