import pandas as pd

from cellphonedb.src.core.utils import filters


def call(genes: pd.DataFrame, gene_columns: list) -> pd.DataFrame:
    genes.rename(index=str, columns={'uniprot': 'name'},
                 inplace=True)

    filters.remove_not_defined_columns(genes, gene_columns + ['name'])

    return genes
