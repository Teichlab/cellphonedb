from tools import app
from tools.generate_data.filters import remove_genes
from utils import utils


def generate_genes_action(gene_base_filename: str, remove_genes_filename: str):
    gene_base_filename = '{}/{}'.format(app.data_dir, gene_base_filename)
    remove_genes_filename = '{}/{}'.format(app.data_dir, remove_genes_filename)

    gene_base_data = utils.read_data_table_from_file(gene_base_filename)
    remove_genes_data = utils.read_data_table_from_file(remove_genes_filename)

    genes_filtered = remove_genes.remove_genes_in_file(gene_base_data, remove_genes_data)

    genes_filtered.to_csv('{}/{}'.format(app.output_dir, 'gene_filtered.csv'), index=False)
