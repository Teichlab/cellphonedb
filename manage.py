import click

from cellphonedb.src.api_endpoints.terminal_api.query_terminal_api_endpoints import query_terminal_commands
from cellphonedb.src.local_launchers.local_collector_launcher import LocalCollectorLauncher
from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.local_launchers.local_exporter_launcher import LocalExporterLauncher
from cellphonedb.src.api_endpoints.terminal_api.method_terminal_api_endpoints import method_terminal_commands

app = create_app()


@app.cli.command
def run():
    app.run()


@app.cli.command()
def create_db():
    cellphonedb_app.cellphonedb.database_manager.database.create_all()


@app.cli.command()
def reset_db():
    database = cellphonedb_app.cellphonedb.database_manager.database
    database.drop_everything()
    database.create_all()


@app.cli.command()
@click.argument('table')
@click.argument('file', default='')
def collect(table, file):
    getattr(LocalCollectorLauncher(), table)(file)


@app.cli.command()
@click.argument('table')
def export(table):
    getattr(LocalExporterLauncher(), table)()


@app.cli.group()
def method():
    pass


@app.cli.group()
def query():
    pass


method.add_command(method_terminal_commands.statistical_analysis)
method.add_command(method_terminal_commands.analysis)
query.add_command(query_terminal_commands.find_interactions_by_element)
query.add_command(query_terminal_commands.get_interaction_gene)
query.add_command(query_terminal_commands.cpdb_data_report)
query.add_command(query_terminal_commands.autocomplete)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
