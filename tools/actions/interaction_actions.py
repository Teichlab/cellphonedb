from tools import app
from tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from utils.utils import read_data_table_from_file


def generate_iuphar_action(iuphar_filename: str, gene_filename: str, protein_filename: str):
    iuphar_original = read_data_table_from_file('{}/{}'.format(app.data_dir, iuphar_filename), dtype=str)

    genes = read_data_table_from_file('{}/{}'.format(app.data_dir, gene_filename), dtype=str)
    proteins = read_data_table_from_file('{}/{}'.format(app.data_dir, protein_filename), dtype=str)

    parse_iuphar_guidetopharmacology.call(iuphar_original, genes, proteins)
