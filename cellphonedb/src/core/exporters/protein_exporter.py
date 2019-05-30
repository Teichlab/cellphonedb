import pandas as pd

from cellphonedb.utils import dataframe_format


def call(proteins_expanded: pd.DataFrame) -> pd.DataFrame:
    proteins_expanded.rename(index=str, columns={'name': 'uniprot'}, inplace=True)
    return proteins_expanded[
        ['uniprot', 'protein_name', 'transmembrane', 'peripheral', 'secreted', 'secreted_desc', 'secreted_highlight',
         'receptor', 'receptor_desc', 'integrin', 'other', 'other_desc', 'tags', 'tags_description', 'tags_reason']]
