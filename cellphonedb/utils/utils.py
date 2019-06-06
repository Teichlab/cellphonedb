import io
import os
import pickle
from typing import TextIO, Optional

import pandas as pd
from werkzeug.datastructures import FileStorage

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import output_dir

from cellphonedb.src.exceptions.NotADataFrameException import NotADataFrameException
from cellphonedb.src.exceptions.ReadFileException import ReadFileException
from cellphonedb.src.exceptions.ReadFromPickleException import ReadFromPickleException


def read_data_table_from_file(file: str, index_column_first: bool = False, separator: str = '',
                              dtype=None, na_values=None, compression=None) -> pd.DataFrame:
    filename, file_extension = os.path.splitext(file)

    if file_extension == '.pickle':
        try:
            with open(file, 'rb') as f:
                df = pickle.load(f)
                if isinstance(df, pd.DataFrame):
                    return df
                else:
                    raise NotADataFrameException(file)
        except:
            raise ReadFromPickleException(file)

    if not separator:
        separator = _get_separator(file_extension)
    try:
        f = open(file)
    except Exception:
        raise ReadFileException(file)
    else:
        with f:
            return _read_data(f, separator, index_column_first, dtype, na_values, compression)


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


def write_to_file(df: pd.DataFrame, filename: str, output_path: str, output_format: Optional[str] = None):
    _, file_extension = os.path.splitext(filename)

    if output_format is None:
        if not file_extension:
            default_format = 'txt'
            default_extension = '.{}'.format(default_format)

            separator = _get_separator(default_extension)
            filename = '{}{}'.format(filename, default_extension)
        else:
            separator = _get_separator(file_extension)
    else:
        selected_extension = '.{}'.format(output_format)

        if file_extension != selected_extension:
            separator = _get_separator(selected_extension)
            filename = '{}{}'.format(filename, selected_extension)

            if file_extension:
                app_logger.warning(
                    'Selected extension missmatches output filename ({}, {}): It will be added => {}'.format(
                        selected_extension, file_extension, filename))
        else:
            separator = _get_separator(selected_extension)

    df.to_csv('{}/{}'.format(output_path, filename), sep=separator, index=False)


def _read_data(file_stream: TextIO, separator: str, index_column_first: bool, dtype=None,
               na_values=None, compression=None) -> pd.DataFrame:
    return pd.read_csv(file_stream, sep=separator, index_col=0 if index_column_first else None, dtype=dtype,
                       na_values=na_values, compression=compression)


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

    return extensions.get(mime_type_or_extension.lower(), default_separator)


def set_paths(output_path, project_name):
    if not output_path:
        output_path = output_dir

    if project_name:
        output_path = os.path.realpath(os.path.expanduser('{}/{}'.format(output_path, project_name)))

    os.makedirs(output_path, exist_ok=True)

    if _path_is_not_empty(output_path):
        app_logger.warning(
            'Output directory ({}) exist and is not empty. Result can overwrite old results'.format(output_path))

    return output_path


def _path_is_not_empty(path):
    return bool([f for f in os.listdir(path) if not f.startswith('.')])