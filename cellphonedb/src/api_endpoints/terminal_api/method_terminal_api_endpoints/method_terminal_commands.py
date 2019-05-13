import sys
import traceback
from typing import Optional
import click

from cellphonedb.src.app import cpdb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.core.exceptions.AllCountsFilteredException import AllCountsFilteredException
from cellphonedb.src.core.exceptions.EmptyResultException import EmptyResultException
from cellphonedb.src.core.exceptions.ThresholdValueException import ThresholdValueException
from cellphonedb.src.core.utils.subsampler import Subsampler
from cellphonedb.src.exceptions.ParseCountsException import ParseCountsException
from cellphonedb.src.exceptions.ParseMetaException import ParseMetaException
from cellphonedb.src.exceptions.ReadFileException import ReadFileException
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher


@click.command()
@click.argument('meta-filename')
@click.argument('counts-filename')
@click.option('--project-name', default='', type=str,
              help='Name of the project. It creates a subfolder in output folder')
@click.option('--iterations', default=1000, type=int, help='Number of pvalues analysis iterations [1000]')
@click.option('--threshold', default=0.1, type=float, help='% of cells expressing a gene')
@click.option('--result-precision', default='3', type=int, help='Number of decimal digits in results [3]')
@click.option('--output-path', default='', type=str,
              help='Directory where the results will be allocated (the directory must exist) [out]')
@click.option('--means-result-name', default='means.txt', type=str, help='Means result namefile [means.txt]')
@click.option('--pvalues-result-name', default='pvalues.txt', type=str, help='Pvalues result namefile [pvalues.txt]')
@click.option('--significant-mean-result-name', default='significant_means.txt', type=str,
              help='Significant result namefile [significant_means.txt]')
@click.option('--pvalue', 'min_significant_mean', default=0.05, type=float,
              help='Pvalue threshold [0.05]')
@click.option('--deconvoluted-result-name', default='deconvoluted.txt',
              help='Deconvoluted result namefile [deconvoluted.txt]')
@click.option('--debug-seed', default='-1', type=int, help='Debug random seed 0 for disable it. >=0 to set it [-1]')
@click.option('--threads', default=4, type=int, help='Max of threads to process the data [4]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
@click.option('--subsampling', default=False, is_flag=True, type=bool, help='Enable subsampling')
@click.option('--subsampling-log', default=None, type=bool,
              help='Enable subsampling log1p for non transformed data inputs')
@click.option('--subsampling-num-pc', default=100, type=int, help='Subsampling NumPC argument')
@click.option('--subsampling-num-cells', default=None, type=int,
              help='Number of cells to subsample (defaults to a 1/3 of cells)')
def statistical_analysis(meta_filename: str,
                         counts_filename: str,
                         project_name: str,
                         iterations: int,
                         threshold: float,
                         result_precision: int,
                         output_path: str,
                         means_result_name: str,
                         pvalues_result_name: str,
                         significant_mean_result_name: str,
                         min_significant_mean: float,
                         deconvoluted_result_name: str,
                         debug_seed: int,
                         threads: int,
                         verbose: bool,
                         subsampling: bool,
                         subsampling_log: bool,
                         subsampling_num_pc: int,
                         subsampling_num_cells: Optional[int]
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
                                                            means_result_name,
                                                            pvalues_result_name,
                                                            significant_mean_result_name,
                                                            deconvoluted_result_name,
                                                            debug_seed,
                                                            threads,
                                                            result_precision,
                                                            min_significant_mean,
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
@click.argument('meta-filename')
@click.argument('counts-filename')
@click.option('--project-name', default='', type=str,
              help='Name of the project. It creates a subfolder in output folder')
@click.option('--threshold', default=0.1, type=float, help='% of cells expressing a gene')
@click.option('--result-precision', default='3', type=int, help='Number of decimal digits in results [3]')
@click.option('--output-path', default='', type=str,
              help='Directory where the results will be allocated (the directory must exist) [out]')
@click.option('--means-result-name', default='means.txt', type=str, help='Means result namefile [means.txt]')
@click.option('--significant-means-result-name', default='significant_means.txt', type=str,
              help='Significant result namefile [significant_means.txt]')
@click.option('--deconvoluted-result-name', default='deconvoluted.txt', type=str,
              help='Deconvoluted result namefile [deconvoluted.txt]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
@click.option('--subsampling', default=False, is_flag=True, type=bool, help='Enable subsampling')
@click.option('--subsampling-log', default=None, is_flag=True, type=bool,
              help='Enable subsampling log1p for non transformed data inputs')
@click.option('--subsampling-num-pc', default=100, type=int, help='Subsampling NumPC argument')
@click.option('--subsampling-num-cells', default=None, type=int,
              help='Number of cells to subsample (defaults to a 1/3 of cells)')
def analysis(meta_filename: str,
             counts_filename: str,
             project_name: str,
             threshold: float,
             result_precision: int,
             output_path: str,
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
