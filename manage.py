import click
from cellphonedb.collection import Collector
from cellphonedb.api import create_app
from cellphonedb.exporter import Exporter
from cellphonedb.extensions import db
from cellphonedb.db_scripts import db_drop_everything
from cellphonedb.FlaskQueryLauncher import FlaskQueryLauncher

app = create_app()


@app.cli.command
def run():
    app.run()


@app.cli.command()
def create_db():
    db.create_all()


@app.cli.command()
def reset_db():
    db_drop_everything(db)
    db.create_all()


@app.cli.command()
@click.argument('table')
@click.argument('file', default='')
def collect(table, file):
    collector = Collector(app)
    # Get the method of the collector that matches the table name and run
    getattr(collector, table)(file)


@app.cli.command()
@click.argument('table')
def export(table):
    exporter = Exporter(app)
    getattr(exporter, table)()


@app.cli.command()
@click.argument('queryname')
@click.argument('files', nargs=-1)
def call_query(queryname, files):
    getattr(FlaskQueryLauncher, queryname)(*files)
