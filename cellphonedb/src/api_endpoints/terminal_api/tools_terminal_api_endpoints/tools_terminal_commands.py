import pandas as pd
from click._unicodefun import click

from cellphonedb.src.app.cellphonedb_app import output_dir, data_dir
from cellphonedb.tools.actions import gene_actions
from cellphonedb.tools.generate_data.filters.non_complex_interactions import only_noncomplex_interactions
from cellphonedb.tools.generate_data.filters.remove_interactions import remove_interactions_in_file
from cellphonedb.tools.generate_data.getters import get_iuphar_guidetopharmacology
from cellphonedb.tools.generate_data.mergers.add_curated import add_curated
from cellphonedb.tools.generate_data.mergers.merge_interactions import merge_iuphar_imex_interactions
from cellphonedb.tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from cellphonedb.tools.generate_data.parsers.parse_interactions_imex import parse_interactions_imex
from cellphonedb.utils import utils


@click.command()
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
        result_path = output_dir

    gene_actions.generate_genes_from_uniprot_ensembl_db(uniprot_db_filename, ensembl_db_filename, proteins_filename,
                                                        gene_uniprot_ensembl_merged_result_filename, result_path)

    gene_actions.add_hla_genes(gene_uniprot_ensembl_merged_result_filename, hla_genes_filename, '', add_hla_result_filename,
                               result_path)

    gene_actions.remove_genes_in_file(add_hla_result_filename, remove_genes_filename, result_filename)

    gene_actions.validate_gene_list(result_filename, result_path)


@click.command()
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
