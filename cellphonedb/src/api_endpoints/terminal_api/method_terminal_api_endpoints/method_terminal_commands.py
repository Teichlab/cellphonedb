import sys
import traceback

import click

from cellphonedb.src.app import cpdb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.core.exceptions.AllCountsFilteredException import AllCountsFilteredException
from cellphonedb.src.core.exceptions.EmptyResultException import EmptyResultException
from cellphonedb.src.core.exceptions.ThresholdValueException import ThresholdValueException
from cellphonedb.src.exceptions.ParseCountsException import ParseCountsException
from cellphonedb.src.exceptions.ParseMetaException import ParseMetaException
from cellphonedb.src.exceptions.ReadFileException import ReadFileException
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher


@click.command()
@click.argument('meta-filename')
@click.argument('counts-filename')
@click.option('--project-name', default='', help='Name of the project. It creates a subfolder in output folder')
@click.option('--iterations', default=1000, help='Number of pvalues analysis iterations [1000]')
@click.option('--threshold', default=0.1, help='% of cells expressing a gene')
@click.option('--result-precision', default='3', help='Number of decimal digits in results [3]')
@click.option('--output-path', default='',
              help='Directory where the results will be allocated (the directory must exist) [out]')
@click.option('--output-format', type=click.Choice(['txt', 'csv', 'tsv', 'tab']))
@click.option('--means-result-name', default='means', help='Means result namefile [means]')
@click.option('--pvalues-result-name', default='pvalues', help='Pvalues result namefile [pvalues]')
@click.option('--significant-mean-result-name', default='significant_means',
              help='Significant result namefile [significant_means]')
@click.option('--deconvoluted-result-name', default='deconvoluted',
              help='Deconvoluted result namefile [deconvoluted]')
@click.option('--pvalue', 'min_significant_mean', default=0.05, type=float,
              help='Pvalue threshold [0.05]')
@click.option('--debug-seed', default='-1', help='Debug random seed 0 for disable it. >=0 to set it [-1]')
@click.option('--threads', default=4, help='Max of threads to process the data [4]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
def statistical_analysis(meta_filename: str,
                         counts_filename: str,
                         project_name: str,
                         iterations: int,
                         threshold: float,
                         result_precision: int,
                         output_path: str,
                         output_format: str,
                         means_result_name: str,
                         pvalues_result_name: str,
                         significant_mean_result_name: str,
                         deconvoluted_result_name: str,
                         min_significant_mean: float,
                         debug_seed: int,
                         threads: int,
                         verbose: bool,
                         ) -> None:
    try:
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
                                                            significant_mean_result_name,
                                                            deconvoluted_result_name,
                                                            debug_seed,
                                                            threads,
                                                            result_precision,
                                                            min_significant_mean,
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
@click.option('--project-name', default='', help='Name of the project. It creates a subfolder in output folder')
@click.option('--threshold', default=0.1, help='% of cells expressing a gene')
@click.option('--result-precision', default='3', help='Number of decimal digits in results [3]')
@click.option('--output-path', default='',
              help='Directory where the results will be allocated (the directory must exist) [out]')
@click.option('--output-format', type=click.Choice(['txt', 'csv', 'tsv', 'tab']))
@click.option('--means-result-name', default='means', help='Means result namefile [means]')
@click.option('--significant-means-result-name', default='significant_means',
              help='Significant result namefile [significant_means]')
@click.option('--deconvoluted-result-name', default='deconvoluted',
              help='Deconvoluted result namefile [deconvoluted]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
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
             verbose: bool
             ):
    try:
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

        if (verbose):
            traceback.print_exc(file=sys.stdout)
