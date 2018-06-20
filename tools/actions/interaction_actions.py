from tools import app
from tools.generate_data.getters import get_iuphar_guidetopharmacology
from tools.generate_data.mergers import merge_interactions
from tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from utils.utils import read_data_table_from_file


def merge_iuphar_imex_action(iuphar_filename: str,
                             gene_filename: str,
                             protein_filename: str,
                             imex_interactions_filename: str,
                             data_path: str = '',
                             processed_iuphar_result_filename: str = 'cellphonedb_interactions_iuphar.csv',
                             result_filename: str = 'iuphar_imex_interactions.csv',
                             result_path: str = '',
                             download_original_path: str = '',
                             default_download_response: str = ''):
    if not result_path:
        result_path = app.output_dir

    if not data_path:
        data_path = app.data_dir

    if not download_original_path:
        download_original_path = app.downloads_dir

    if not default_download_response:
        default_download_response = None

    iuphar_original = get_iuphar_guidetopharmacology.call(iuphar_filename, data_path, download_original_path,
                                                          default_download_response)

    genes = read_data_table_from_file('{}/{}'.format(data_path, gene_filename), dtype=str)
    proteins = read_data_table_from_file('{}/{}'.format(data_path, protein_filename), dtype=str)
    imex_interactions = read_data_table_from_file('{}/{}'.format(data_path, imex_interactions_filename), dtype=str)

    iuphar_interactions = parse_iuphar_guidetopharmacology.call(iuphar_original, genes, proteins)

    iuphar_interactions.to_csv('{}/{}'.format(result_path, processed_iuphar_result_filename), index=False)

    merged_interactions = merge_interactions.merge_iuphar_imex_interactions(iuphar_interactions, imex_interactions)

    merged_interactions.sort_values(['source', 'uniprot_1', 'uniprot_2']).to_csv(
        '{}/{}'.format(result_path, result_filename), index=False)
