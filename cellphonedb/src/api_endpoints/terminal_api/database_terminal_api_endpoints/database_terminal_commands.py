import os
from datetime import datetime
from typing import Optional

import click
from click import Context

from cellphonedb.src.api_endpoints.terminal_api.tools_terminal_api_endpoints.tools_terminal_commands import \
    generate_proteins, generate_complex, _set_paths, generate_interactions, filter_all, generate_genes
from cellphonedb.src.app.cellphonedb_app import output_dir
from cellphonedb.src.database.manager import DatabaseVersionManager
from cellphonedb.src.database.manager.DatabaseVersionManager import collect_database
from cellphonedb.utils.utils import set_paths


@click.command()
@click.option('--database', default='cellphone_custom_{}.db'.format(datetime.now().strftime("%Y-%m-%d-%H_%M")),
              help='output file name [cellphone_custom_<current date_time>.db]')
@click.option('--result-path', default='', help='output folder for the collected database')
def collect(database, result_path):
    output_path = set_paths(output_dir, result_path)

    DatabaseVersionManager.collect_database(database, output_path)


@click.command()
@click.option('--version', type=str, default='latest')
def download(version: str):
    DatabaseVersionManager.download_database(version)


@click.command()
def list_remote():
    DatabaseVersionManager.list_remote_database_versions()


@click.command()
def list_local():
    DatabaseVersionManager.list_local_database_versions()


@click.command()
@click.option('--user-protein', type=click.Path(file_okay=True, exists=True, dir_okay=False))
@click.option('--user-gene', type=click.Path(file_okay=True, exists=True, dir_okay=False))
@click.option('--user-complex', type=click.Path(file_okay=True, exists=True, dir_okay=False))
@click.option('--user-interactions', type=click.Path(file_okay=True, exists=True, dir_okay=False))
@click.option('--fetch', is_flag=True)
@click.option('--result-path', type=str, default=None)
@click.option('--log-file', type=str, default='log.txt')
@click.pass_context
def generate(ctx: Context,
             user_protein: Optional[str],
             user_gene: Optional[str],
             user_complex: Optional[str],
             user_interactions: Optional[str],
             fetch: bool,
             result_path: Optional[str],
             log_file: str
             ):
    ctx.invoke(generate_proteins, user_protein=user_protein, fetch_uniprot=fetch, result_path=result_path,
               log_file=log_file)
    ctx.invoke(generate_genes, user_gene=user_gene, fetch_uniprot=fetch, fetch_ensembl=fetch, result_path=result_path,
               log_file=log_file)
    ctx.invoke(generate_complex, user_complex=user_complex, result_path=result_path, log_file=log_file)

    output_path = _set_paths(output_dir, result_path)

    proteins_file = os.path.join(output_path, 'protein_generated.csv')
    genes_file = os.path.join(output_path, 'gene_generated.csv')
    complex_file = os.path.join(output_path, 'complex_generated.csv')

    ctx.invoke(generate_interactions, proteins=proteins_file, genes=genes_file, complex=complex_file,
               user_interactions=user_interactions, result_path=result_path, fetch_imex=fetch, fetch_iuphar=fetch)

    ctx.invoke(filter_all, input_path=output_path, result_path=result_path)

    db_name = 'cellphonedb_user_{}.db'.format(datetime.now().strftime("%Y-%m-%d-%H_%M"))

    collect_database(db_name, output_path,
                     protein_filename='protein_input.csv',
                     gene_filename='gene_input.csv',
                     complex_filename='complex_input.csv',
                     interaction_filename='interaction_input.csv',
                     data_path=output_path)
