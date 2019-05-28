import pandas as pd


def call(complex_compositions: pd.DataFrame, complex_name: str) -> pd.DataFrame:
    complex_elements = complex_compositions[complex_compositions['name_complex'] == complex_name]
    complex_elements = complex_elements[
        ['name_complex', 'name_protein', 'protein_name_protein', 'gene_name_protein']].drop_duplicates()
    return complex_elements
