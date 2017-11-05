import click

from flask.cli import FlaskGroup
from tools.app import create_app
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.merge_gene_mouse import merge_gene_mouse as merge_gene
from tools.interaction_actions import generate_inweb_interactions as protein_generate_inweb, \
    only_noncomplex_interactions, remove_interactions_in_file, append_curated


def create_tools_app(info):
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_tools_app)
def cli():
    pass


@cli.command()
@click.argument('filename', default='protein.csv')
def merge_duplicated_proteins(filename):
    merge_proteins(filename)


@cli.command()
@click.argument('dilename_gene')
@click.argument('filename_gene_mouse')
def merge_gene_mouse(filename_gene, filename_gene_mouse):
    merge_gene(filename_gene, filename_gene_mouse)


@cli.command()
@click.argument('inweb_inbiomap_namefile', default='')
@click.argument('database_proteins_namefile', default='protein.csv')
def generate_inweb(inweb_inbiomap_namefile, database_proteins_namefile):
    protein_generate_inweb(inweb_inbiomap_namefile, database_proteins_namefile)


@cli.command()
@click.argument('complex_namefile', default='complex.csv')
@click.argument('inweb_namefile', default='cellphone_inweb.csv')
def generate_inweb_noncomplex(complex_namefile, inweb_namefile):
    only_noncomplex_interactions(complex_namefile, inweb_namefile)


@cli.command()
@click.argument('interaction_namefile', default='cellphone_inweb.csv')
@click.argument('interaction_to_remove_namefile', default='remove_interactions.csv')
def remove_interactions(interaction_namefile, interaction_to_remove_namefile):
    remove_interactions_in_file(interaction_namefile, interaction_to_remove_namefile)


@cli.command()
@click.argument('interaction_namefile', default='interactions_cleaned.csv')
@click.argument('interaction_curated_namefile', default='interaction_curated.csv')
def add_curated(interaction_namefile, interaction_curated_namefile):
    append_curated(interaction_namefile, interaction_curated_namefile)


if __name__ == "__main__":
    cli()
