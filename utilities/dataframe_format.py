def bring_columns_to_start(columns, dataframe):
    """

    :type columns: list
    :type dataframe: pd.DataFrame
    :rtype: pd.DataFrame
    """
    column_headers = list(dataframe.columns.values)
    for column in reversed(columns):
        column_headers.insert(0, column_headers.pop(column_headers.index(column)))

    result = dataframe.ix[:, column_headers]
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

    result = dataframe.ix[:, column_headers]
    return result
