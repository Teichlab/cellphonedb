import click
from cellphonedb.flask_terminal_collector_launcher import FlaskTerminalCollectorLauncher
from cellphonedb.flask_app import create_app
from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.flask_terminal_optimiezer_launcher import FlaskTerminalOptimizerLauncher
from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.flask_terminal_exporter_launcher import FlaskTerminalExporterLauncher

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
def optimize(table):
    getattr(FlaskTerminalOptimizerLauncher(), table)()


@app.cli.command()
@click.argument('table')
@click.argument('file', default='')
def collect(table, file):
    getattr(FlaskTerminalCollectorLauncher(), table)(file)


@app.cli.command()
@click.argument('table')
def export(table):
    getattr(FlaskTerminalExporterLauncher(), table)()


@app.cli.command()
@click.argument('queryname')
@click.argument('files', nargs=-1)
def call_query(queryname, files):
    getattr(FlaskTerminalQueryLauncher(), queryname)(*files)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
