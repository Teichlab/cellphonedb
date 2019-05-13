import os
from typing import Optional

import click
import pandas as pd
from rpy2 import robjects

from cellphonedb.src.exceptions.MissingPlotterFunctionException import MissingPlotterFunctionException


def plot(plot_function, results_path, rows, columns):
    os.chdir(results_path)

    means_df = pd.read_csv('./means.txt', sep='\t')
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

    robjects.r('library(ggplot2)')

    plotter = robjects.r[function_name]

    plotter(width=int(5 + max(3, n_cols * 0.8)),
            height=int(5 + max(5, n_rows * 0.5)),
            selected_rows=selected_rows,
            selected_columns=selected_columns
            )


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
