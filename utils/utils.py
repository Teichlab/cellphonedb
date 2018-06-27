import os
from typing import TextIO

import pandas as pd


def read_data_table_from_file(file: str, index_column_first: bool = False, separator: str = '',
                              dtype=None) -> pd.DataFrame:
    filename, file_extension = os.path.splitext(file)
    if not separator:
        separator = _get_separator(file_extension)
    with open(file) as f:
        return _read_data(f, separator, index_column_first, dtype)


# TODO: set file type
def read_data_from_content_type(file, index_column_first=False, separator: str = '', dtype=None) -> pd.DataFrame:
    if not separator:
        separator = _get_separator(file.content_type)
    return _read_data(file.stream, separator, index_column_first, dtype)


def _read_data(file_stream: TextIO, separator: str, index_column_first: bool, dtype=None) -> pd.DataFrame:
    return pd.read_csv(file_stream, sep=separator, index_col=0 if index_column_first else None, dtype=dtype)


def _get_separator(mime_type_or_extension: str) -> str:
    extensions = {
        '.csv': ',',
        '.tsv': '\t',
        '.txt': '\t',
        '.tab': '\t',
        'text/csv': ',',
        'text/tab-separated-values': '\t',
    }
    default_separator = ','

    if mime_type_or_extension in extensions:
        return extensions[mime_type_or_extension]

    return default_separator
