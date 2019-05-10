import os
import sys
import traceback
from typing import Optional, Any, Callable

import click
import pandas as pd
from rpy2 import robjects
from rpy2.robjects.vectors import StrVector
from click import Context

from cellphonedb.src.app import cpdb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.core.exceptions.AllCountsFilteredException import AllCountsFilteredException
from cellphonedb.src.core.exceptions.EmptyResultException import EmptyResultException
from cellphonedb.src.core.exceptions.ThresholdValueException import ThresholdValueException
from cellphonedb.src.core.utils.subsampler import Subsampler
from cellphonedb.src.exceptions.MissingPlotterFunctoinException import MissingPlotterFunctionException
from cellphonedb.src.exceptions.ParseCountsException import ParseCountsException
from cellphonedb.src.exceptions.ParseMetaException import ParseMetaException
from cellphonedb.src.exceptions.ReadFileException import ReadFileException
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher


def check_subsampling_params(ctx: Context, argument: click.Argument, value) -> Any:
    subsampling = ctx.params.get('subsampling')

    if not subsampling and value is not None:
        tpl = 'This parameter ({}) only applies to subsampling, to enable it add `--subsampling` to your command'
        app_logger.error(tpl.format(argument.name))
        ctx.abort()

    if argument.name == 'subsampling_log' and subsampling and value is None:
        app_logger.error('''In order to perform subsampling you need to specify whether to log1p input counts or not:
            to do this specify in your command as --subsampling-log [true|false]''')
        ctx.abort()

    defaults = {
        'subsampling_num_pc': 100,
        'subsampling_num_cells': None
    }

    if subsampling and value is None:
        return defaults.get(argument.name, None)

    return value


def subsampling_options(f: Callable) -> Callable:
    options = [
        click.option('--subsampling', is_flag=True, help='Enable subsampling', is_eager=True),
        click.option('--subsampling-log', default=None, type=bool, callback=check_subsampling_params,
                     help='Enable subsampling log1p for non transformed data inputs !mandatory!'),
        click.option('--subsampling-num-pc', default=None, type=int, callback=check_subsampling_params,
                     help='Subsampling NumPC argument [100]'),
        click.option('--subsampling-num-cells', default=None, type=int, callback=check_subsampling_params,
                     help='Number of cells to subsample (defaults to a 1/3 of cells)')
    ]

    for option in reversed(options):
        f = option(f)

    return f


def common_options(f: Callable) -> Callable:
    options = [
        click.argument('meta-filename'),
        click.argument('counts-filename'),
        click.option('--project-name', default='', type=str,
                     help='Name of the project. It creates a subfolder in output folder'),
        click.option('--threshold', default=0.1, type=float, help='% of cells expressing a gene'),
        click.option('--result-precision', default='3', type=int, help='Number of decimal digits in results [3]'),
        click.option('--output-path', default='', type=str,
                     help='Directory where the results will be allocated (the directory must exist) [out]'),
        click.option('--output-format', type=click.Choice(['txt', 'csv', 'tsv', 'tab'])),
        click.option('--means-result-name', default='means', type=str, help='Means result namefile [means]'),
        click.option('--significant-means-result-name', default='significant_means', type=str,
                     help='Significant result namefile [significant_means]'),
        click.option('--deconvoluted-result-name', default='deconvoluted',
                     help='Deconvoluted result namefile [deconvoluted]'),
        click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]'),
        subsampling_options
    ]

    for option in reversed(options):
        f = option(f)

    return f


@click.command()
@common_options
@click.option('--debug-seed', default='-1', type=int, help='Debug random seed 0 for disable it. >=0 to set it [-1]')
@click.option('--pvalue', default=0.05, type=float, help='Pvalue threshold [0.05]')
@click.option('--pvalues-result-name', default='pvalues', type=str, help='Pvalues result namefile [pvalues]')
@click.option('--iterations', default=1000, type=int, help='Number of pvalues analysis iterations [1000]')
@click.option('--threads', default=4, type=int, help='Max of threads to process the data [4]')
def statistical_analysis(meta_filename: str,
                         counts_filename: str,
                         project_name: str,
                         threshold: float,
                         result_precision: int,
                         output_path: str,
                         output_format: str,
                         means_result_name: str,
                         significant_means_result_name: str,
                         deconvoluted_result_name: str,
                         verbose: bool,
                         subsampling: bool,
                         subsampling_log: bool,
                         subsampling_num_pc: int,
                         subsampling_num_cells: Optional[int],
                         debug_seed: int,
                         pvalue: float,
                         pvalues_result_name: str,
                         iterations: int,
                         threads: int
                         ) -> None:
    try:

        subsampler = Subsampler(subsampling_log,
                                subsampling_num_pc,
                                subsampling_num_cells,
                                verbose) if subsampling else None

        LocalMethodLauncher(cpdb_app.create_app(verbose)). \
            cpdb_statistical_analysis_local_method_launcher(meta_filename,
                                                            counts_filename,
                                                            project_name,
                                                            iterations,
                                                            threshold,
                                                            output_path,
                                                            output_format,
                                                            means_result_name,
                                                            pvalues_result_name,
                                                            significant_means_result_name,
                                                            deconvoluted_result_name,
                                                            debug_seed,
                                                            threads,
                                                            result_precision,
                                                            pvalue,
                                                            subsampler,
                                                            )
    except (ReadFileException, ParseMetaException, ParseCountsException, ThresholdValueException,
            AllCountsFilteredException) as e:
        app_logger.error(str(e) +
                         (':' if (hasattr(e, 'description') and e.description) or (
                                 hasattr(e, 'hint') and e.hint) else '') +
                         (' {}.'.format(e.description) if hasattr(e, 'description') and e.description else '') +
                         (' {}.'.format(e.hint) if hasattr(e, 'hint') and e.hint else '')
                         )

    except EmptyResultException as e:
        app_logger.warning(str(e) +
                           (':' if (hasattr(e, 'description') and e.description) or (
                                   hasattr(e, 'hint') and e.hint) else '') +
                           (' {}.'.format(e.description) if hasattr(e, 'description') and e.description else '') +
                           (' {}.'.format(e.hint) if hasattr(e, 'hint') and e.hint else '')
                           )
    except:
        app_logger.error('Unexpected error')
        if verbose:
            traceback.print_exc(file=sys.stdout)


@click.command()
@common_options
def analysis(meta_filename: str,
             counts_filename: str,
             project_name: str,
             threshold: float,
             result_precision: int,
             output_path: str,
             output_format: str,
             means_result_name: str,
             significant_means_result_name: str,
             deconvoluted_result_name: str,
             verbose: bool,
             subsampling: bool,
             subsampling_log: bool,
             subsampling_num_pc: int,
             subsampling_num_cells: Optional[int]
             ):
    try:

        subsampler = Subsampler(subsampling_log,
                                subsampling_num_pc,
                                subsampling_num_cells,
                                verbose) if subsampling else None

        LocalMethodLauncher(cpdb_app.create_app(verbose)).cpdb_analysis_local_method_launcher(meta_filename,
                                                                                              counts_filename,
                                                                                              project_name,
                                                                                              threshold,
                                                                                              output_path,
                                                                                              output_format,
                                                                                              means_result_name,
                                                                                              significant_means_result_name,
                                                                                              deconvoluted_result_name,
                                                                                              result_precision,
                                                                                              subsampler,
                                                                                              )
    except (ReadFileException, ParseMetaException, ParseCountsException, ThresholdValueException,
            AllCountsFilteredException) as e:
        app_logger.error(str(e) +
                         (':' if (hasattr(e, 'description') and e.description) or (
                                 hasattr(e, 'hint') and e.hint) else '') +
                         (' {}.'.format(e.description) if hasattr(e, 'description') and e.description else '') +
                         (' {}.'.format(e.hint) if hasattr(e, 'hint') and e.hint else '')
                         )

    except EmptyResultException as e:
        app_logger.warning(str(e) +
                           (':' if (hasattr(e, 'description') and e.description) or (
                                   hasattr(e, 'hint') and e.hint) else '') +
                           (' {}.'.format(e.description) if hasattr(e, 'description') and e.description else '') +
                           (' {}.'.format(e.hint) if hasattr(e, 'hint') and e.hint else '')
                           )
    except:
        app_logger.error('Unexpected error')

        if verbose:
            traceback.print_exc(file=sys.stdout)


@click.command()
@click.option('--rows', type=click.File('r'))
@click.option('--columns', type=click.File('r'))
@click.option('--plot-function', type=str, default='dot_plot')
def plot(rows, columns, plot_function):
    os.chdir('./out')

    means_df = pd.read_csv('./means.txt', sep='\t')
    n_rows, n_cols = means_df.shape
    n_cols -= 9

    n_rows, selected_rows = selected_items(rows, n_rows)
    n_cols, selected_columns = selected_items(columns, n_cols)

    this_file_dir = os.path.dirname(os.path.realpath(__file__))

    robjects.r.source(os.path.join(this_file_dir, 'plotters/plot_dot_by_column_name.R'))
    available_names = list(robjects.globalenv.keys())

    if plot_function in available_names:
        function_name = plot_function
    else:
        raise MissingPlotterFunctionException()

    robjects.r('library(ggplot2)')

    dot_plot = robjects.r[function_name]
    dot_plot(width=int(5 + max(3, n_cols * 0.8)), height=int(5 + max(5, n_rows * 0.5)), selected_rows=selected_rows)


def selected_items(selection: Optional[click.File], size):
    if selection is not None:
        df = pd.read_csv(selection, header=None)
        names = df[0].tolist()

        selected_rows = StrVector(names)
        size = len(names)
    else:
        selected_rows = robjects.NULL

    return size, selected_rows
