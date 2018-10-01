import click
import os
import pandas as pd

from flask.cli import FlaskGroup

from tools import app
from tools.actions import gene_actions, interaction_actions
from tools.app import create_app, data_dir, output_dir
from tools.generate_data.getters import get_iuphar_guidetopharmacology
from tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.generate_data.mergers.add_curated import add_curated
from tools.generate_data.mergers.merge_interactions import merge_interactions, merge_iuphar_imex_interactions
from tools.generate_data.filters.remove_interactions import remove_interactions_in_file
from tools.generate_data.filters.non_complex_interactions import only_noncomplex_interactions
from tools.generate_data.parsers.parse_interactions_inweb import generate_interactions_inweb as protein_generate_inweb
from tools.generate_data.parsers.parse_interactions_imex import parse_interactions_imex
from cellphonedb.utils import utils


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
@click.argument('inweb_inbiomap_filename', default='')
@click.argument('database_proteins_filename', default='protein.csv')
def inweb_interactions(inweb_inbiomap_filename, database_proteins_filename):
    protein_generate_inweb(inweb_inbiomap_filename, database_proteins_filename)


@cli.command()
@click.argument('imex_original_filename')
@click.argument('database_proteins_filename', default='protein.csv')
@click.argument('database_gene_filename', default='gene.csv')
def imex_interactions(imex_original_filename, database_proteins_filename, database_gene_filename):
    interactions_base_df = pd.read_csv('%s/%s' % (data_dir, imex_original_filename), sep='\t', na_values='-')
    protein_df = pd.read_csv('%s/%s' % (data_dir, database_proteins_filename))
    gene_df = pd.read_csv('%s/%s' % (data_dir, database_gene_filename))

    result = parse_interactions_imex(interactions_base_df, protein_df, gene_df)

    result.to_csv('%s/cellphone_interactions_imex.csv' % output_dir, index=False)


@cli.command()
@click.argument('interactions_filename_1')
@click.argument('interactions_filename_2')
def merge_interactions(interactions_filename_1, interactions_filename_2):
    interactions_1 = _open_file(interactions_filename_1)
    interactions_2 = _open_file(interactions_filename_2)

    result = merge_interactions(interactions_1, interactions_2)

    result.to_csv('%s/cellphone_interactions.csv' % output_dir, index=False)


@cli.command()
@click.argument('interactions_filename')
@click.argument('database_complex_filename', default='complex.csv')
def remove_complex_interactions(interactions_filename, database_complex_filename):
    interactions = pd.read_csv(_open_file(interactions_filename))
    complexes = pd.read_csv(_open_file(database_complex_filename))
    result = only_noncomplex_interactions(interactions, complexes)

    result.to_csv('%s/no_complex_interactions.csv' % (output_dir), index=False, float_format='%.4f')


@cli.command()
@click.argument('interaction_filename')
@click.argument('interaction_to_remove_filename', default='remove_interactions.csv')
def remove_interactions(interaction_filename, interaction_to_remove_filename):
    interactions = pd.read_csv(_open_file(interaction_filename))
    interactions_to_remove = pd.read_csv(_open_file(interaction_to_remove_filename))

    result = remove_interactions_in_file(interactions, interactions_to_remove)
    result.to_csv('%s/clean_interactions.csv' % (output_dir), index=False)


@cli.command()
@click.argument('interaction_filename', default='clean_interactions.csv')
@click.argument('interaction_curated_filename', default='interaction_curated.csv')
def add_curated_interactions(interaction_filename, interaction_curated_filename):
    interaction = pd.read_csv(_open_file(interaction_filename), dtype={'iuphar': pd.np.bool})
    interaction_curated = pd.read_csv(_open_file(interaction_curated_filename), dtype={'iuphar': pd.np.bool})

    result = add_curated(interaction, interaction_curated)
    result.to_csv('%s/interaction.csv' % output_dir, index=False)


@cli.command()
@click.argument('imex_raw_filename')
@click.argument('iuphar_raw_filename')
@click.argument('database_proteins_filename', default='protein.csv')
@click.argument('database_gene_filename', default='gene.csv')
@click.argument('database_complex_filename', default='complex.csv')
@click.argument('interaction_to_remove_filename')
@click.argument('interaction_curated_filename')
def generate_interactions(
        imex_raw_filename: str,
        iuphar_raw_filename: str,
        database_proteins_filename: str,
        database_gene_filename: str,
        database_complex_filename: str,
        interaction_to_remove_filename: str,
        interaction_curated_filename: str) -> None:
    interactions_base = utils.read_data_table_from_file('%s/%s' % (data_dir, imex_raw_filename), na_values='-')
    proteins = pd.read_csv('%s/%s' % (data_dir, database_proteins_filename))
    genes = pd.read_csv('%s/%s' % (data_dir, database_gene_filename))
    complexes = pd.read_csv('%s/%s' % (data_dir, database_complex_filename))
    interactions_to_remove = pd.read_csv('%s/%s' % (data_dir, interaction_to_remove_filename))
    interaction_curated = pd.read_csv('%s/%s' % (data_dir, interaction_curated_filename))

    print('generating imex file')
    imex_interactions = parse_interactions_imex(interactions_base, proteins, genes)

    print('Getting Iuphar interactions')

    iuphar_original = get_iuphar_guidetopharmacology.call(iuphar_raw_filename, data_dir,
                                                          '{}/downloads'.format(data_dir),
                                                          default_download_response='yes')
    print('generating iuphar file')
    iuphar_interactions = parse_iuphar_guidetopharmacology.call(iuphar_original, genes, proteins)

    print('merging iuphar/imex')
    merged_interactions = merge_iuphar_imex_interactions(iuphar_interactions, imex_interactions)

    print('removing complex interactions')
    no_complex_interactions = only_noncomplex_interactions(merged_interactions, complexes)

    print('removing selected interactions')
    clean_interactions = remove_interactions_in_file(no_complex_interactions, interactions_to_remove)

    print('adding curated interaction')
    interactions_with_curated = add_curated(clean_interactions, interaction_curated)

    interactions_with_curated.to_csv('%s/interaction.csv' % output_dir, index=False)


@cli.command()
@click.argument('iuphar_filename')
@click.argument('gene_filename')
@click.argument('protein_filename')
@click.argument('imex_interactions_filename')
@click.argument('data_path', default='')
@click.argument('processed_iuphar_result_filename', default='cellphonedb_interactions_iuphar.csv')
@click.argument('result_filename', default='iuphar_imex_interactions.csv')
@click.argument('result_path', default='')
@click.argument('download_original_path', default='')
@click.argument('default_download_response', default='')
def merge_iuphar_imex(iuphar_filename: str,
                      gene_filename: str,
                      protein_filename: str,
                      imex_interactions_filename: str,
                      data_path: str,
                      processed_iuphar_result_filename: str,
                      result_filename: str,
                      result_path: str,
                      download_original_path: str,
                      default_download_response):
    interaction_actions.merge_iuphar_imex_action(iuphar_filename, gene_filename, protein_filename,
                                                 imex_interactions_filename, data_path,
                                                 processed_iuphar_result_filename, result_filename, result_path,
                                                 download_original_path, default_download_response)


@cli.command()
@click.argument('uniprot_db_filename')
@click.argument('ensembl_db_filename')
@click.argument('proteins_filename')
@click.argument('remove_genes_filename')
@click.argument('hla_genes_filename')
@click.option('--result_filename', default='gene.csv')
@click.option('--result_path', default='')
@click.option('--gene_uniprot_ensembl_merged_result_filename', default='gene_uniprot_ensembl_merged.csv')
@click.option('--add_hla_result_filename', default='gene_hla_added.csv')
def generate_genes(
        uniprot_db_filename: str,
        ensembl_db_filename: str,
        proteins_filename: str,
        remove_genes_filename: str,
        hla_genes_filename: str,
        result_filename: str,
        result_path: str,
        gene_uniprot_ensembl_merged_result_filename: str,
        add_hla_result_filename: str) -> None:
    if not result_path:
        result_path = app.output_dir

    gene_actions.generate_genes_from_uniprot_ensembl_db(uniprot_db_filename, ensembl_db_filename, proteins_filename,
                                                        gene_uniprot_ensembl_merged_result_filename, result_path)

    merge_result_filename = '{}/{}'.format('../out', gene_uniprot_ensembl_merged_result_filename)
    gene_actions.add_hla_genes(merge_result_filename, hla_genes_filename, '', add_hla_result_filename,
                               result_path)

    add_hla_result_filename = '{}/{}'.format('../out', add_hla_result_filename)
    gene_actions.remove_genes_in_file(add_hla_result_filename, remove_genes_filename, result_filename)

    gene_actions.validate_gene_list(result_filename, result_path)


@cli.command()
@click.argument('gene_base_filename')
@click.argument('remove_genes_filename', default='')
@click.argument('result_filename', default='gene.csv')
def remove_genes_in_file(gene_base_filename: str,
                         remove_genes_filename: str,
                         result_filename: str):
    gene_actions.remove_genes_in_file(gene_base_filename, remove_genes_filename, result_filename)


@cli.command()
@click.argument('uniprot_db_filename')
@click.argument('ensembl_db_filename')
@click.argument('proteins_filename')
@click.argument('result_filename', default='gene_uniprot_ensembl_merged.csv')
@click.argument('result_path', default='')
def generate_genes_from_uniprot_ensembl_db(uniprot_db_filename: str,
                                           ensembl_db_filename: str,
                                           proteins_filename: str,
                                           result_filename: str,
                                           result_path: str):
    gene_actions.generate_genes_from_uniprot_ensembl_db(uniprot_db_filename, ensembl_db_filename, proteins_filename,
                                                        result_filename, result_path)


def _open_file(interaction_filename):
    if os.path.isfile('%s/%s' % (data_dir, interaction_filename)):
        return os.path.join(data_dir, interaction_filename)

    return os.path.join(output_dir, interaction_filename)


if __name__ == "__main__":
    cli()
