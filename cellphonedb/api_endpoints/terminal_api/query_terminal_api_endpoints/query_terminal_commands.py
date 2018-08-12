from click._unicodefun import click

from cellphonedb.local_launchers.local_query_launcher import LocalQueryLauncher


@click.command()
@click.argument('element')
def find_interactions_by_element(element: str):
    LocalQueryLauncher.find_interactions_by_element(element)


@click.command()
@click.option('--columns', default=None, help='Columns to set in the result')
def get_interaction_gene(columns: str):
    LocalQueryLauncher.get_interaction_gene(columns)


@click.command()
def cpdb_data_report():
    LocalQueryLauncher.cpdb_data_report()
