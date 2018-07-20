import pandas as pd


def call(columns: list, interactions: pd.DataFrame, complex_composition: pd.DataFrame) -> pd.DataFrame:
    if not columns:
        columns = ['gene_name', 'name', 'hgnc_symbol', 'ensembl']

    genes_1 = _get_genes_by_suffix(columns, '_1', interactions)
    genes_2 = _get_genes_by_suffix(columns, '_2', interactions)

    genes = genes_1.append(genes_2).dropna().drop_duplicates().reset_index(drop=True)

    interactions_names = interactions[interactions['is_complex_1']]['name_1'].append(
        interactions[interactions['is_complex_2']]['name_2']).tolist()

    complex_composition_filtered = complex_composition[
        complex_composition['name_complex'].apply(
            lambda name_complex: name_complex in interactions_names)].drop_duplicates()

    genes = genes.append(
        _get_genes_by_suffix(columns, '_protein', complex_composition_filtered)).drop_duplicates().reset_index(
        drop=True)

    return genes


def _get_genes_by_suffix(columns: list, suffix: str, interactions: pd.DataFrame):
    suffixed_columns = ['{}{}'.format(column, suffix) for column in columns]
    genes = pd.DataFrame()

    genes[columns] = interactions[suffixed_columns]

    return genes
