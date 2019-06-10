import os
import tempfile
from typing import Optional

import pandas as pd
from rpy2 import situation

from cellphonedb.src.exceptions.MissingPlotterFunctionException import MissingPlotterFunctionException
from cellphonedb.src.exceptions.MissingR import MissingR
from cellphonedb.src.exceptions.RRuntimeException import RRuntimeException
from cellphonedb.utils.utils import _get_separator

try:
    if not situation.get_r_home() or not situation.r_version_from_subprocess():
        raise MissingR()

    from rpy2 import robjects
    from rpy2.rinterface_lib.embedded import RRuntimeError
except MissingR as e:
    raise e


def heatmaps_plot(meta_file: str,
                  pvalues_file: str,
                  output_path: str,
                  count_name: str,
                  log_name: str
                  ) -> None:
    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    robjects.r.source(os.path.join(this_file_dir, 'R/plot_heatmaps.R'))
    available_names = list(robjects.globalenv.keys())
    count_filename = os.path.join(output_path, count_name)
    log_filename = os.path.join(output_path, log_name)
    plot_function: str = 'heatmaps_plot'

    with open(pvalues_file, 'rt') as original:
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(pvalues_file)[-1], mode='wt', encoding='utf8') as new:
            line = original.readline().replace('.', '_').replace('|', '.')
            new.write(line)
            for line in original.readlines():
                new.write(line)

            if plot_function in available_names:
                function_name = plot_function
            else:
                raise MissingPlotterFunctionException()

            plotter = robjects.r[function_name]

            try:
                plotter(meta_file=meta_file,
                        pvalues_file=new.name,
                        count_filename=count_filename,
                        log_filename=log_filename
                        )
            except RRuntimeError as e:
                raise RRuntimeException(e)


def dot_plot(means_path: str,
             pvalues_path: str,
             output_path: str,
             output_name: str,
             rows: Optional[str] = None,
             columns: Optional[str] = None
             ) -> None:
    pvalues_separator = _get_separator(os.path.splitext(pvalues_path)[-1])
    means_separator = _get_separator(os.path.splitext(means_path)[-1])
    output_extension = os.path.splitext(output_name)[-1].lower()
    filename = os.path.join(output_path, output_name)

    means_df = pd.read_csv(means_path, sep=means_separator)
    n_rows, n_cols = means_df.shape
    n_cols -= 10

    n_rows, selected_rows = selected_items(rows, n_rows)
    n_cols, selected_columns = selected_items(columns, n_cols)

    this_file_dir = os.path.dirname(os.path.realpath(__file__))
    robjects.r.source(os.path.join(this_file_dir, 'R/plot_dot_by_column_name.R'))
    available_names = list(robjects.globalenv.keys())
    plot_function: str = 'dot_plot'

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


def selected_items(selection: Optional[str], size):
    if selection is not None:
        df = pd.read_csv(selection, header=None)
        names = df[0].tolist()

        from rpy2.robjects.vectors import StrVector
        selected = StrVector(_sanitize_names(names))
        size = len(names)
    else:
        selected = robjects.NULL

    return size, selected


def _sanitize_names(names):
    return [name.replace('|', '.') for name in names]
