import click

from flask.cli import FlaskGroup
from tools.app import create_app
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.merge_gene_mouse import merge_gene_mouse as merge_gene
from tools.interaction_actions import generate_inweb_interactions as protein_generate_inweb, \
    only_noncomplex_interactions


def create_tools_app(info):
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_tools_app)
def cli():
    pass


@cli.command()
@click.argument('filename')
def merge_duplicated_proteins(filename):
    merge_proteins(filename)


@cli.command()
@click.argument('dilename_gene')
@click.argument('filename_gene_mouse')
def merge_gene_mouse(filename_gene, filename_gene_mouse):
    merge_gene(filename_gene, filename_gene_mouse)


@cli.command()
@click.argument('database_proteins', default='protein.csv')
@click.argument('inweb_inbiomap_file', default='core.psimitab')
def generate_inweb(database_proteins, inweb_inbiomap_file):
    protein_generate_inweb(database_proteins, inweb_inbiomap_file)


@cli.command()
@click.argument('complexes_namefile', default='complex.csv')
@click.argument('inweb_namefile', default='cellphone_inweb.csv')
def generate_inweb_noncomplex(complexes_namefile, inweb_namefile):
    only_noncomplex_interactions(complexes_namefile, inweb_namefile)


if __name__ == "__main__":
    cli()
