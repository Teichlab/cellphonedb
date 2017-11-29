import click
import os
import pandas as pd

from flask.cli import FlaskGroup
from tools.app import create_app, data_dir, output_dir
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.merge_gene_mouse import merge_gene_mouse as merge_gene
from tools.generate_data.mergers.add_curated import add_curated
from tools.generate_data.mergers.merge_interactions import merge_interactions
from tools.generate_data.filters.remove_interactions import remove_interactions_in_file
from tools.generate_data.filters.non_complex_interactions import only_noncomplex_interactions
from tools.generate_data.parsers.parse_interactions_inweb import generate_interactions_inweb as protein_generate_inweb
from tools.generate_data.parsers.parse_interactions_innatedb import generate_interactions_innatedb
from tools.generate_data.parsers.parse_interactions_imex import parse_interactions_imex


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
@click.argument('imex_original_namefile')
@click.argument('database_proteins_namefile', default='protein.csv')
@click.argument('database_gene_namefile', default='gene.csv')
def imex_interactions(imex_original_namefile, database_proteins_namefile, database_gene_namefile):
    interactions_base_df = pd.read_csv('%s/%s' % (data_dir, imex_original_namefile), sep='\t', na_values='-')
    protein_df = pd.read_csv('%s/%s' % (data_dir, database_proteins_namefile))
    gene_df = pd.read_csv('%s/%s' % (data_dir, database_gene_namefile))

    result = parse_interactions_imex(interactions_base_df, protein_df, gene_df)

    result.to_csv('%s/cellphone_interactions_imex.csv' % output_dir, index=False)


@cli.command()
@click.argument('innatedb_namefile', default='innatedb_ppi.mitab')
@click.argument('database_gene_namefile', default='gene.csv')
def innatedb_interactions(innatedb_namefile, database_gene_namefile):
    generate_interactions_innatedb(innatedb_namefile, database_gene_namefile)


@cli.command()
@click.argument('interactions_namefile_1')
@click.argument('interactions_namefile_2')
def merge_interactions(interactions_namefile_1, interactions_namefile_2):
    interactions_1 = _open_file(interactions_namefile_1)
    interactions_2 = _open_file(interactions_namefile_2)

    result = merge_interactions(interactions_1, interactions_2)

    result.to_csv('%s/cellphone_interactions.csv' % output_dir, index=False)


@cli.command()
@click.argument('interactions_namefile')
@click.argument('database_complex_namefile', default='complex.csv')
def noncomplex_interactions(interactions_namefile, database_complex_namefile):
    interactions = pd.read_csv(_open_file(interactions_namefile))
    complexes = pd.read_csv(_open_file(database_complex_namefile))

    result = only_noncomplex_interactions(interactions, complexes)

    result.to_csv('%s/no_complex_interactions.csv' % (output_dir), index=False, float_format='%.4f')


@cli.command()
@click.argument('interaction_namefile', default='no_complex_interactions.csv')
@click.argument('interaction_to_remove_namefile', default='remove_interactions.csv')
def remove_interactions(interaction_namefile, interaction_to_remove_namefile):
    remove_interactions_in_file(interaction_namefile, interaction_to_remove_namefile)


@cli.command()
@click.argument('interaction_namefile', default='clean_interactions.csv')
@click.argument('interaction_curated_namefile', default='interaction_curated.csv')
def add_curated_interactions(interaction_namefile, interaction_curated_namefile):
    interaction = pd.read_csv(_open_file(interaction_namefile))
    interaction_curated = pd.read_csv(_open_file(interaction_curated_namefile))

    result = add_curated(interaction, interaction_curated)
    result.to_csv('%s/interaction.csv' % output_dir, index=False)


@cli.command()
@click.argument('imex_original_namefile')
@click.argument('database_proteins_namefile', default='protein.csv')
@click.argument('database_gene_namefile', default='gene.csv')
@click.argument('database_complex_namefile', default='complex.csv')
def generate_interactions(imex_original_namefile, database_proteins_namefile, database_gene_namefile,
                          database_complex_namefile):
    interactions_base = pd.read_csv('%s/%s' % (data_dir, imex_original_namefile), sep='\t', na_values='-')
    proteins = pd.read_csv('%s/%s' % (data_dir, database_proteins_namefile))
    genes = pd.read_csv('%s/%s' % (data_dir, database_gene_namefile))
    complexes = pd.read_csv('%s/%s' % (data_dir, database_complex_namefile))

    imex_interactions = parse_interactions_imex(interactions_base, proteins, genes)

    only_noncomplex_interactions(imex_interactions, complexes)


def _open_file(interaction_namefile):
    if os.path.isfile('%s/%s' % (data_dir, interaction_namefile)):
        return os.path.join(data_dir, interaction_namefile)

    return os.path.join(output_dir, interaction_namefile)


if __name__ == "__main__":
    cli()
