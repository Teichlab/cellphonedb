from tools import app
from tools.generate_data.filters import remove_genes
from tools.generate_data.mergers import mergers_genes
from utils import utils


def remove_genes_in_file(gene_base_filename: str, remove_genes_filename: str,
                         result_filename: str = 'gene_filtered.csv') -> None:
    gene_base_filename = '{}/{}'.format(app.data_dir, gene_base_filename)
    remove_genes_filename = '{}/{}'.format(app.data_dir, remove_genes_filename)

    gene_base_data = utils.read_data_table_from_file(gene_base_filename)
    remove_genes_data = utils.read_data_table_from_file(remove_genes_filename)

    genes_filtered = remove_genes.remove_genes_in_file(gene_base_data, remove_genes_data)

    genes_filtered.to_csv('{}/{}'.format(app.output_dir, result_filename), index=False)


def generate_genes_from_uniprot_ensembl_db(uniprot_db_filename: str, ensembl_db_filename: str, proteins_filename: str,
                                           result_filename: str = 'gene_uniprot_ensembl_merged.csv',
                                           result_path: str = ''):
    uniprot_db_filename = '{}/{}'.format(app.data_dir, uniprot_db_filename)
    ensembl_db_filename = '{}/{}'.format(app.data_dir, ensembl_db_filename)
    proteins_filename = '{}/{}'.format(app.data_dir, proteins_filename)

    if not result_path:
        result_path = app.output_dir

    uniprots = utils.read_data_table_from_file(uniprot_db_filename)
    ensembls = utils.read_data_table_from_file(ensembl_db_filename)
    proteins = utils.read_data_table_from_file(proteins_filename)

    result = mergers_genes.merge_genes_from_uniprot_ensembl_db(ensembls, proteins, uniprots)

    result.to_csv('{}/{}'.format(result_path, result_filename), index=False)
