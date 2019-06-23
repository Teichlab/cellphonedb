import pandas as pd

from cellphonedb.src.core.utils import filters


def call(proteins: pd.DataFrame, multidata_colums, protein_columns):
    bools = ['transmembrane', 'secreted', 'peripheral', 'receptor', 'other', 'secreted_highlight']

    proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)
    proteins[bools] = proteins[bools].astype(bool)

    proteins = _optimizations(proteins)
    multidatas_to_add = process_multidata_data(proteins, multidata_colums)
    proteins_to_add = process_protein_data(proteins, protein_columns)

    return proteins_to_add, multidatas_to_add


def _optimizations(proteins):
    proteins['is_complex'] = False
    return proteins


def process_multidata_data(proteins: pd.DataFrame, multidata_columns: list) -> pd.DataFrame:
    multidata_proteins = proteins.copy()
    return filters.remove_not_defined_columns(multidata_proteins, multidata_columns)


def process_protein_data(proteins: pd.DataFrame, protein_columns: list) -> pd.DataFrame:
    proteins = proteins.copy()
    proteins = filters.remove_not_defined_columns(proteins, protein_columns + ['name'])
    return proteins
