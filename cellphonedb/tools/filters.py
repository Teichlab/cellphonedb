import pandas as pd


def remove_not_defined_columns(data_frame: pd.DataFrame, defined_columns: list) -> pd.DataFrame:
    """

    :type data_frame: pd.DataFrame
    :type defined_columns: list
    :rtype: pd.DataFrame
    """
    data_frame_keys = list(data_frame.keys())

    for key in data_frame_keys:
        if key not in defined_columns:
            data_frame.drop(key, axis=1, inplace=True)

    return data_frame
