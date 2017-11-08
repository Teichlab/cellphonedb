import click
from flask.cli import FlaskGroup

from cellcommdb.collection import Collector
from cellcommdb.api import create_app
from cellcommdb.exporter import Exporter
from cellcommdb.extensions import db
from cellcommdb.db_scripts import db_drop_everything
from cellcommdb.models import *
from cellcommdb.query_manager import Queries


def create_cellphone_app(info):
    return create_app()


app = create_cellphone_app(None)


@click.group(cls=FlaskGroup, create_app=create_cellphone_app)
def cli():
    pass


@cli.command
def run():
    app.run()


@cli.command()
def create_db():
    db.create_all()


@cli.command()
def reset_db():
    db_drop_everything(db)
    db.create_all()


@cli.command()
@click.argument('table')
@click.argument('file', default='')
def collect(table, file):
    collector = Collector(app)
    # Get the method of the collector that matches the table name and run
    getattr(collector, table)(file)


@cli.command()
@click.argument('table')
def export(table):
    exporter = Exporter(app)
    getattr(exporter, table)()


@cli.command()
@click.argument('queryname')
@click.argument('files', nargs=-1)
def call_query(queryname, files):
    queries = Queries(app)
    getattr(queries, queryname)(*files)


if __name__ == "__main__":
    cli()
