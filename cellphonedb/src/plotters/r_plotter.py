import os
from functools import wraps
from typing import Optional

import pandas as pd

from cellphonedb.src.exceptions.MissingPlotterFunctionException import MissingPlotterFunctionException
from cellphonedb.src.exceptions.MissingR import MissingR
from cellphonedb.src.exceptions.RRuntimeException import RRuntimeException
from cellphonedb.utils.utils import _get_separator


def ensure_R_setup():
    from rpy2 import situation
    try:
        if not situation.get_r_home() or not situation.r_version_from_subprocess():
            raise MissingR()

    except MissingR as e:
        raise e


def _ensure_path_exists(path: str) -> None:
    expanded_path = os.path.expanduser(path)

    if not os.path.exists(expanded_path):
        os.makedirs(expanded_path)


def with_r_setup(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ensure_R_setup()

        from rpy2.rinterface_lib.embedded import RRuntimeError
        from rpy2 import robjects

        return f(*args, **kwargs, robjects=robjects, r_runtime_error=RRuntimeError)

    return wrapper


@with_r_setup
def heatmaps_plot(*,
                  meta_file: str,
                  pvalues_file: str,
                  output_path: str,
                  count_name: str,
                  log_name: str,
                  count_network_filename: str,
                  interaction_count_filename: str,
                  pvalue: float,
                  robjects,
                  r_runtime_error: Exception
                  ) -> None:
    _ensure_path_exists(output_path)
    meta_file_separator = _get_separator(os.path.splitext(meta_file)[-1])
    pvalues_file_separator = _get_separator(os.path.splitext(pvalues_file)[-1])
    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    robjects.r.source(os.path.join(this_file_dir, 'R/plot_heatmaps.R'))
    available_names = list(robjects.globalenv.keys())
    count_filename = os.path.join(output_path, count_name)
    log_filename = os.path.join(output_path, log_name)
    plot_function = 'heatmaps_plot'

    if plot_function in available_names:
        function_name = plot_function
    else:
        raise MissingPlotterFunctionException()

    plotter = robjects.r[function_name]

    count_network_separator = _get_separator(os.path.splitext(count_network_filename)[-1])
    interaction_count_separator = _get_separator(os.path.splitext(interaction_count_filename)[-1])

    count_network_filename = os.path.join(output_path, count_network_filename)
    interaction_count_filename = os.path.join(output_path, interaction_count_filename)

    try:
        plotter(meta_file=meta_file,
                pvalues_file=pvalues_file,
                count_filename=count_filename,
                log_filename=log_filename,
                count_network_filename=count_network_filename,
                interaction_count_filename=interaction_count_filename,
                count_network_separator=count_network_separator,
                interaction_count_separator=interaction_count_separator,
                meta_sep=meta_file_separator,
                pvalues_sep=pvalues_file_separator,
                pvalue=pvalue,
                )
    except r_runtime_error as e:
        raise RRuntimeException(e)


@with_r_setup
def dot_plot(*,
             means_path: str,
             pvalues_path: str,
             output_path: str,
             output_name: str,
             robjects,
             r_runtime_error: Exception,
             rows: Optional[str] = None,
             columns: Optional[str] = None
             ) -> None:
    _ensure_path_exists(output_path)
    pvalues_separator = _get_separator(os.path.splitext(pvalues_path)[-1])
    means_separator = _get_separator(os.path.splitext(means_path)[-1])
    output_extension = os.path.splitext(output_name)[-1].lower()
    filename = os.path.join(output_path, output_name)

    means_df = pd.read_csv(means_path, sep=means_separator)
    n_rows, n_cols = means_df.shape
    n_cols -= 11

    n_rows, selected_rows = selected_items(rows, n_rows)
    n_cols, selected_columns = selected_items(columns, n_cols)

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    robjects.r.source(os.path.join(this_file_dir, 'R/plot_dot_by_column_name.R'))
    available_names = list(robjects.globalenv.keys())
    plot_function = 'dot_plot'

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
    except r_runtime_error as e:
        raise RRuntimeException(e)


@with_r_setup
def selected_items(selection: Optional[str], size, *, robjects, r_runtime_error):
    if selection is not None:
        df = pd.read_csv(selection, header=None)
        names = df[0].tolist()

        from rpy2.robjects.vectors import StrVector
        selected = StrVector(names)
        size = len(names)
    else:
        selected = robjects.NULL

    return size, selected
