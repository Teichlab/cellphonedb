import pandas as pd

from cellphonedb.core.models.multidata import properties_multidata
from cellphonedb.core.utils import filters


def call(proteins: pd.DataFrame, multidata_colums, protein_columns):
    bools = ['transmembrane', 'secretion', 'peripheral', 'receptor',
             'receptor_highlight', 'adhesion', 'other', 'transporter',
             'secreted_highlight', 'iuhpar_ligand', 'cytoplasm', 'extracellular']

    proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)
    proteins[bools] = proteins[bools].astype(bool)

    proteins = _optimizations(proteins)
    multidatas_to_add = process_multidata_data(proteins, multidata_colums)
    proteins_to_add = process_protein_data(proteins, protein_columns)

    return proteins_to_add, multidatas_to_add


def _optimizations(proteins):
    proteins['is_complex'] = False
    proteins['is_cellphone_receptor'] = proteins.apply(lambda protein: properties_multidata.is_receptor(protein),
                                                       axis=1)
    return proteins


def process_multidata_data(proteins: pd.DataFrame, multidata_columns: list) -> pd.DataFrame:
    multidata_proteins = proteins.copy()
    return filters.remove_not_defined_columns(multidata_proteins, multidata_columns)


def process_protein_data(proteins: pd.DataFrame, protein_columns: list) -> pd.DataFrame:
    proteins = proteins.copy()
    proteins = filters.remove_not_defined_columns(proteins, protein_columns + ['name'])
    return proteins
