from tools import app
from tools.generate_data.getters import get_iuphar_guidetopharmacology
from tools.generate_data.mergers import merge_interactions
from tools.generate_data.parsers import parse_iuphar_guidetopharmacology
from utils.utils import read_data_table_from_file


def merge_iuphar_action(iuphar_filename: str, gene_filename: str, protein_filename: str, interactions_filename: str):
    # get_iuphar_guidetopharmacology.call('interaction_iuphar_guidetopharmacology__20180616.csv', 'tools/data/downloads')
    #
    # return

    iuphar_original = read_data_table_from_file('{}/{}'.format(app.data_dir, iuphar_filename), dtype=str)

    genes = read_data_table_from_file('{}/{}'.format(app.data_dir, gene_filename), dtype=str)
    proteins = read_data_table_from_file('{}/{}'.format(app.data_dir, protein_filename), dtype=str)
    original_interactions = read_data_table_from_file('{}/{}'.format(app.data_dir, interactions_filename), dtype=str)

    iuphar_interactions = parse_iuphar_guidetopharmacology.call(iuphar_original, genes, proteins)

    from tools.repository.interaction import interaction_exist
    curated_interactions = read_data_table_from_file(
        '{}/interaction_curated_20180614.csv'.format(app.data_dir, iuphar_filename), dtype=str)
    curated_interactions.rename(columns={'multidata_name_1': 'uniprot_1', 'multidata_name_2': 'uniprot_2'}, index=str,
                                inplace=True)

    iuphar_interactions_not_in_1 = iuphar_interactions[
        ~iuphar_interactions.apply(lambda row: interaction_exist(row, curated_interactions, 'uniprot_1', 'uniprot_2'),
                                   axis=1) == False]

    print(iuphar_interactions_not_in_1)

    print(len(original_interactions))
    print(len(iuphar_interactions))
    merged = merge_interactions.merge_iuphar_interactions(original_interactions, iuphar_interactions)
    print(len(merged))
