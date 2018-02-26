import os
from typing import TextIO

import pandas as pd


def read_data_table_from_file(file: str, index_column_first: bool = False, separator: str = '') -> pd.DataFrame:
    filename, file_extension = os.path.splitext(file)
    if not separator:
        separator = _get_separator(file_extension)
    return _read_data(open(file), separator, index_column_first)


# TODO: set file type
def read_data_from_mime(file, index_column_first=False, separator: str = '') -> pd.DataFrame:
    if not separator:
        separator = _get_separator(file.content_type)
    return _read_data(file.stream, separator, index_column_first)


def _read_data(file_stream: TextIO, separator: str, index_column_first: bool) -> pd.DataFrame:
    return pd.read_csv(file_stream, sep=separator, index_col=0 if index_column_first else None)


def _get_separator(mime_type_or_extension: str) -> str:
    extensions = {
        '.csv': ',',
        '.tsv': '\t',
        '.txt': '\t',
        'text/csv': ',',
        'text/tab-separated-values': '\t',
    }
    default_separator = ','

    if mime_type_or_extension in extensions:
        return extensions[mime_type_or_extension]

    return default_separator
