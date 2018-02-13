import click
from cellphonedb.flaskcollectorlauncher import FlaskCollectorLauncher
from cellphonedb.api import create_app
from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.FlaskQueryLauncher import FlaskQueryLauncher
from cellphonedb.flaskexporterlauncher import FlaskExporterLauncher

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
    getattr(FlaskCollectorLauncher(), table)(file)


@app.cli.command()
@click.argument('table')
def export(table):
    getattr(FlaskExporterLauncher(), table)()


@app.cli.command()
@click.argument('queryname')
@click.argument('files', nargs=-1)
def call_query(queryname, files):
    getattr(FlaskQueryLauncher, queryname)(*files)
