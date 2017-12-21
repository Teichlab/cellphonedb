import click
from flask.cli import FlaskGroup

from cellcommdb.collection import Collector
from cellcommdb.api import create_app
from cellcommdb.exporter import Exporter
from cellcommdb.extensions import db
from cellcommdb.db_scripts import db_drop_everything
from cellcommdb.query_manager import QueryLauncher

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
    queries = QueryLauncher(app)
    getattr(queries, queryname)(*files)
