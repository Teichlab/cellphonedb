import pandas as pd


def call(columns, interactions):
    interactions = interactions.dropna(subset=['ensembl_1', 'ensembl_2'], how='any')

    if not columns:
        columns = ['gene_name', 'name', 'hgnc_symbol', 'ensembl']

    genes_1 = _get_genes_by_suffix(columns, '_1', interactions)
    genes_2 = _get_genes_by_suffix(columns, '_2', interactions)

    genes = genes_1.append(genes_2).dropna().drop_duplicates().reset_index(drop=True)

    return genes


def _get_genes_by_suffix(columns: list, suffix: str, interactions: pd.DataFrame):
    suffixed_columns = ['{}{}'.format(column, suffix) for column in columns]
    genes = pd.DataFrame()

    genes[columns] = interactions[suffixed_columns]

    return genes
