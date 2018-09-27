from click._unicodefun import click

from src.local_launchers.local_query_launcher import LocalQueryLauncher
from src.app.cellphonedb_app import cellphonedb_app


@click.command()
@click.argument('element')
def find_interactions_by_element(element: str):
    LocalQueryLauncher(cellphonedb_app).find_interactions_by_element(element)


@click.command()
@click.option('--columns', default=None, help='Columns to set in the result')
def get_interaction_gene(columns: str):
    LocalQueryLauncher(cellphonedb_app).get_interaction_gene(columns)


@click.command()
def cpdb_data_report():
    LocalQueryLauncher(cellphonedb_app).cpdb_data_report()
