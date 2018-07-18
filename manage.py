import click

from cellphonedb.api_endpoints.terminal_api.query_terminal_api_endpoints import query_terminal_commands
from cellphonedb.flask_terminal_collector_launcher import FlaskTerminalCollectorLauncher
from cellphonedb.flask_app import create_app
from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.flask_terminal_exporter_launcher import FlaskTerminalExporterLauncher
from cellphonedb.api_endpoints.terminal_api.method_terminal_api_endpoints import method_terminal_commands

app = create_app()


@app.cli.command
def run():
    app.run()


@app.cli.command()
def create_db():
    cellphonedb_flask.cellphonedb.database_manager.database.create_all()


@app.cli.command()
def reset_db():
    database = cellphonedb_flask.cellphonedb.database_manager.database
    database.drop_everything()
    database.create_all()


@app.cli.command()
@click.argument('table')
@click.argument('file', default='')
def collect(table, file):
    getattr(FlaskTerminalCollectorLauncher(), table)(file)


@app.cli.command()
@click.argument('table')
def export(table):
    getattr(FlaskTerminalExporterLauncher(), table)()


@app.cli.group()
def method():
    pass


@app.cli.group()
def query():
    pass


method.add_command(method_terminal_commands.cluster_statistical_analysis)
query.add_command(query_terminal_commands.search_interactions)
query.add_command(query_terminal_commands.get_interaction_gene)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
