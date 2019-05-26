import os
from typing import Optional

import click
import pandas as pd
from rpy2 import robjects
from rpy2.rinterface_lib.embedded import RRuntimeError

from cellphonedb.src.exceptions.MissingPlotterFunctionException import MissingPlotterFunctionException
from cellphonedb.src.exceptions.RRuntimeException import RRuntimeException
from cellphonedb.utils.utils import _get_separator

def plot(means_path: str,
         pvalues_path: str,
         output_path: str,
         output_name: str,
         rows: click.File,
         columns: click.File,
         plot_function: str,
         ) -> None:
    pvalues_separator = _get_separator(os.path.splitext(pvalues_path)[-1])
    means_separator = _get_separator(os.path.splitext(means_path)[-1])
    output_extension = os.path.splitext(output_name)[-1].lower()
    filename = os.path.join(output_path, output_name)

    means_df = pd.read_csv(means_path, sep=means_separator)
    n_rows, n_cols = means_df.shape
    n_cols -= 9

    n_rows, selected_rows = selected_items(rows, n_rows)
    n_cols, selected_columns = selected_items(columns, n_cols)

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    robjects.r.source(os.path.join(this_file_dir, 'R/plot_dot_by_column_name.R'))
    available_names = list(robjects.globalenv.keys())

    if plot_function in available_names:
        function_name = plot_function
    else:
        raise MissingPlotterFunctionException()

    plotter = robjects.r[function_name]

    try:
        plotter(selected_rows=selected_rows,
                selected_columns=selected_columns,
                filename=filename,
                width=int(5 + max(3, n_cols * 0.8)),
                height=int(5 + max(5, n_rows * 0.5)),
                means_path=means_path,
                pvalues_path=pvalues_path,
                means_separator=means_separator,
                pvalues_separator=pvalues_separator,
                output_extension=output_extension
                )
    except RRuntimeError as e:
        raise RRuntimeException(e)


def selected_items(selection: Optional[click.File], size):
    if selection is not None:
        df = pd.read_csv(selection, header=None)
        names = df[0].tolist()

        from rpy2.robjects.vectors import StrVector
        selected = StrVector(names)
        size = len(names)
    else:
        selected = robjects.NULL

    return size, selected
