import click
from flask.cli import FlaskGroup

from cellcommdb.collection import Collector
from cellcommdb.api import create_app
from cellcommdb.exporter import Exporter
from cellcommdb.extensions import db
from cellcommdb.db_scripts import db_drop_everything
from cellcommdb.models import *
from cellcommdb.query_manager import Queries
from cellcommdb.repository.complex import check_uniprots_are_part_of_complex


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
def call_query(queryname):
    queries = Queries(app)

    getattr(queries, queryname)()


@cli.command()
def custom():
    proteins = ['P16284', 'P01889', 'P01891', 'P01892', 'P03989', 'P04439', 'P05534', 'P10314', 'P13746', 'P16189',
                'P18462', 'P18463', 'P18464', 'P18465', 'P30443', 'P30447', 'P30450', 'P30453', 'P30455', 'P30456',
                'P30460', 'P30461', 'P30462', 'P30464', 'P30466', 'P30475', 'P30480', 'P30483', 'P30484', 'P30485',
                'P30486', 'P30487', 'P30488', 'P30491', 'P30492', 'P30493', 'P30495', 'P30498', 'P30499', 'P30501',
                'P30504', 'P30505', 'P30508', 'P30510', 'P30512', 'P30685', 'Q04826', 'Q07000', 'Q29836', 'Q29940',
                'Q29963', 'Q31612', 'Q95365', 'Q9TNN7', 'Q5TFQ8', 'P01258', 'A6NMY6', 'P01871', 'P01880', 'P01911',
                'P01912', 'P04229', 'P13760', 'P13761', 'P20039', 'P54317', 'P58400', 'Q30134', 'Q30167', 'Q5Y7A7',
                'Q95IE3', 'P01782', 'A0A0C4DH73', 'P04430', 'P01594', 'P01597', 'P01611', 'P01593', 'P04432',
                'A0A075B6P5', 'P06310', 'P01615', 'A0A075B6S6', 'P01614', 'P01624', 'P01619', 'A0A0C4DH25', 'P01703',
                'P01699', 'P01700', 'P01706', 'P01704', 'P01705', 'P01709', 'P01715', 'P01714', 'P80748', 'P01717',
                'P01718', 'P01721', 'P04211', 'Q96KV6', 'A8MVZ5', 'A6NJW9', 'Q5VZ89', 'O15255', 'P01893', 'H3BQJ8',
                'Q96D31', 'Q96SB3', 'Q7RTY9', 'Q9Y6D0', 'Q9NPR2', 'O14492', 'A8MVG2', 'P51864', 'Q8NH08', 'Q8NGN7',
                'P0C629', 'Q8NGY7', 'Q8NGC8', 'P0DN82', 'Q8NH95', 'P0DN81', 'Q8NHC6', 'P47884', 'Q8WZA6', 'Q8NHA8',
                'Q96R84', 'Q8NH06', 'P59922', 'Q8NGU4', 'A6NFC9', 'Q8NHA6', 'P47883', 'Q8NGN8', 'P0C604', 'A6NMZ5',
                'P0C645', 'Q96R72', 'P0C623', 'A6NMU1', 'Q8NGJ3', 'Q8NGH6', 'Q8NH57', 'P0C646', 'Q8NGI1', 'P0C628',
                'Q8NH89', 'P0C617', 'P0C626', 'P0DN80', 'Q8NGA2', 'Q6IF36', 'P0DMU2', 'P0C7N1', 'Q8NGU1', 'P0C7N8',
                'Q9UBW5', 'Q14184', 'O42043', 'O71037', 'P61565', 'P61566', 'Q69384', 'Q902F8', 'Q9UKH3', 'P84996',
                'Q5JWF2', 'Q902F9', 'Q9HB19', 'P63092', 'O75044', 'A6NER0', 'P60507', 'P87889', 'Q9YNA8', 'P62683',
                'P63145', 'P61570', 'Q9HDB9', 'Q7LDI9', 'P61567', 'P63130', 'P62685', 'P63126', 'P63128', 'Q9NX77',
                'P60509', 'P61550', 'P62684', 'Q9N2J8', 'Q9N2K0', 'A0A0B4J1V1', 'A0A0A0MS15', 'P18089', 'P31995',
                'Q96P88', 'Q8NGA4', 'Q8NHK3', 'Q14954', 'Q14953', 'Q99463', 'Q9UMZ3', 'P34925', 'Q9P1P4', 'P04435',
                'P01850', 'A0A5B9', 'B7Z8K6', 'P0CF51', 'P03986', 'Q8TDU5', 'Q7Z5H4', 'Q86SQ3', 'Q9BXE9', 'A6NKC4',
                'Q4G0T1', 'Q96TA0', 'Q9Y5G9', 'A6NMB1', 'Q9Y493', 'Q6UY09', 'O15197', 'Q9NVD7', 'Q6ZSM3', 'P25063']

    check_uniprots_are_part_of_complex(proteins)


if __name__ == "__main__":
    cli()
