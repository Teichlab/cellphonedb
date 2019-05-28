import pandas as pd


def call(complexes: pd.DataFrame) -> pd.DataFrame:
    complexes.rename(index=str, columns={'complex_name': 'name'}, inplace=True)

    complexes.rename(index=str, columns={'uniprot_1': 'protein_1', 'uniprot_2': 'protein_2', 'uniprot_3': 'protein_3',
                                         'uniprot_4': 'protein_4'},
                     inplace=True)

    return complexes
