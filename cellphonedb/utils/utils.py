import io
import os
from typing import TextIO

import pandas as pd
from werkzeug.datastructures import FileStorage

from cellphonedb.src.exceptions.ReadFileException import ReadFileException


def read_data_table_from_file(file: str, index_column_first: bool = False, separator: str = '',
                              dtype=None, na_values=None) -> pd.DataFrame:
    filename, file_extension = os.path.splitext(file)
    if not separator:
        separator = _get_separator(file_extension)
    try:
        f = open(file)
    except Exception:
        raise ReadFileException(file)
    else:
        with f:
            return _read_data(f, separator, index_column_first, dtype, na_values)


def read_data_from_content_type(file: FileStorage, index_column_first: bool = False, separator: str = '',
                                dtype=None) -> pd.DataFrame:
    if not separator:
        separator = _get_separator(file.content_type)
    return _read_data(file.stream, separator, index_column_first, dtype)


def read_data_from_s3_object(s3_object: dict, s3_name: str, index_column_first: bool = False, separator: str = '',
                             dtype=None, na_values=None) -> pd.DataFrame:
    filename, file_extension = os.path.splitext(s3_name)
    if not separator:
        separator = _get_separator(file_extension)
        bytestream = io.BytesIO(s3_object['Body'].read())

    return _read_data(bytestream, separator, index_column_first, dtype, na_values)


def _read_data(file_stream: TextIO, separator: str, index_column_first: bool, dtype=None,
               na_values=None) -> pd.DataFrame:
    return pd.read_csv(file_stream, sep=separator, index_col=0 if index_column_first else None, dtype=dtype,
                       na_values=na_values)


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

    if mime_type_or_extension.lower() in extensions:
        return extensions[mime_type_or_extension.lower()]

    return default_separator
