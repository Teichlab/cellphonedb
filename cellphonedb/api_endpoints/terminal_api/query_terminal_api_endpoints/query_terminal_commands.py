from click._unicodefun import click

from cellphonedb.flask_local_query_launcher import FlaskLocalQueryLauncher


@click.command()
@click.argument('input')
def search_interactions(input: str):
    FlaskLocalQueryLauncher.search_interactions(input)
