import click
import pandas as pd

from flask.cli import FlaskGroup
from tools.app import create_app, data_dir
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.merge_gene_mouse import merge_gene_mouse as merge_gene
from tools.interaction_actions import generate_interactions_inweb as protein_generate_inweb, \
    only_noncomplex_interactions, remove_interactions_in_file, append_curated, \
    generate_interactions_imex, generate_interactions_innatedb, merge_interactions_action, generate_interactions_custom


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
def inweb_interactions(inweb_inbiomap_namefile, database_proteins_namefile):
    protein_generate_inweb(inweb_inbiomap_namefile, database_proteins_namefile)


@cli.command()
@click.argument('interaction_namefile')
@click.argument('database_proteins_namefile', default='protein.csv')
@click.argument('database_gene_namefile', default='gene.csv')
def custom_interactions(interaction_namefile, database_proteins_namefile, database_gene_namefile):
    interactions_base_df = pd.read_csv('%s/%s' % (data_dir, interaction_namefile), sep='\t', na_values='-')
    protein_df = pd.read_csv('%s/%s' % (data_dir, database_proteins_namefile))
    gene_df = pd.read_csv('%s/%s' % (data_dir, database_gene_namefile))

    generate_interactions_custom(interactions_base_df, protein_df, gene_df)


@cli.command()
@click.argument('imex_namefile', default='interaction_imex.txt')
@click.argument('database_proteins_namefile', default='protein.csv')
def imex_interactions(imex_namefile, database_proteins_namefile):
    generate_interactions_imex(imex_namefile, database_proteins_namefile)


@cli.command()
@click.argument('innatedb_namefile', default='innatedb_ppi.mitab')
@click.argument('database_gene_namefile', default='gene.csv')
def innatedb_interactions(innatedb_namefile, database_gene_namefile):
    generate_interactions_innatedb(innatedb_namefile, database_gene_namefile)


@cli.command()
@click.argument('interactions_namefile_1')
@click.argument('interactions_namefile_2')
def merge_interactions(interactions_namefile_1, interactions_namefile_2):
    merge_interactions_action(interactions_namefile_1, interactions_namefile_2)


@cli.command()
@click.argument('complex_namefile', default='complex.csv')
@click.argument('cellphone_namefile', default='cellphone_interactions.csv')
def noncomplex_interactions(complex_namefile, cellphone_namefile):
    only_noncomplex_interactions(complex_namefile, cellphone_namefile)


@cli.command()
@click.argument('interaction_namefile', default='no_complex_interactions.csv')
@click.argument('interaction_to_remove_namefile', default='remove_interactions.csv')
def remove_interactions(interaction_namefile, interaction_to_remove_namefile):
    remove_interactions_in_file(interaction_namefile, interaction_to_remove_namefile)


@cli.command()
@click.argument('interaction_namefile', default='clean_interactions.csv')
@click.argument('interaction_curated_namefile', default='interaction_curated.csv')
def add_curated_interactions(interaction_namefile, interaction_curated_namefile):
    append_curated(interaction_namefile, interaction_curated_namefile)


if __name__ == "__main__":
    cli()
