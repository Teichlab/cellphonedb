from click._unicodefun import click

from cellphonedb.flask_local_query_launcher import FlaskLocalQueryLauncher


@click.command()
@click.argument('input')
def search_interactions(input: str):
    FlaskLocalQueryLauncher.search_interactions(input)


@click.command()
@click.option('--columns', default=None, help='Columns to set in the result')
def get_interaction_gene(columns: str):
    FlaskLocalQueryLauncher.get_interaction_gene(columns)
