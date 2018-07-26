from click._unicodefun import click

from cellphonedb.flask_local_query_launcher import FlaskLocalQueryLauncher


@click.command()
@click.argument('element')
def find_interactions_by_element(element: str):
    FlaskLocalQueryLauncher.find_interactions_by_element(element)


@click.command()
@click.option('--columns', default=None, help='Columns to set in the result')
def get_interaction_gene(columns: str):
    FlaskLocalQueryLauncher.get_interaction_gene(columns)
