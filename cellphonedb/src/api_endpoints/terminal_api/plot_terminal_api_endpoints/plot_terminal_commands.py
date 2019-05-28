import sys
import traceback

import click

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.exceptions.RRuntimeException import RRuntimeException
from cellphonedb.src.plotters import r_plotter


@click.command()
@click.option('--means-path', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              default='./out/means.txt', help='Analysis output means [./out/means.txt]')
@click.option('--pvalues-path', type=click.Path(exists=True, file_okay=True, dir_okay=False),
              default='./out/pvalues.txt', help='Analysis output pvalues [./out/pvalues.txt]')
@click.option('--output-path', type=click.Path(exists=True, file_okay=False, writable=True),
              default='./out', help='Path to write generated plot [./out]')
@click.option('--output-name', type=str, default='./plot.pdf', help='Output file with plot [plot.pdf]')
@click.option('--rows', type=click.File('r'), help='List of rows to plot, one per line [all available]')
@click.option('--columns', type=click.File('r'), help='List of columns to plot, one per line [all available]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
def dot_plot(means_path, pvalues_path, output_path, output_name, rows, columns, verbose):
    print(__name__)
    try:
        r_plotter.plot(means_path, pvalues_path, output_path, output_name, rows, columns, 'dot_plot')
    except RRuntimeException as e:
        app_logger.error(str(e))
    except:
        app_logger.error('Unexpected error')

        if verbose:
            traceback.print_exc(file=sys.stdout)
        else:
            app_logger.error('execute with --verbose to see full stack trace')
