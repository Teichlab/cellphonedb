from datetime import datetime

import click

from cellphonedb.src.app.cellphonedb_app import output_dir
from cellphonedb.src.database.manager import DatabaseVersionManager
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
