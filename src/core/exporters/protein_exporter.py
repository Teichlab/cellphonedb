import pandas as pd

from utils import dataframe_format


def call(proteins_expanded: pd.DataFrame) -> pd.DataFrame:
    proteins_expanded = proteins_expanded.drop(['id_multidata', 'id_protein', 'protein_multidata_id'], axis=1)

    proteins_expanded.rename(index=str, columns={'name': 'uniprot'}, inplace=True)

    proteins_expanded = dataframe_format.bring_columns_to_start(['uniprot'], proteins_expanded)
    proteins_expanded = dataframe_format.bring_columns_to_end(['tags', 'tags_reason'], proteins_expanded)

    return proteins_expanded
