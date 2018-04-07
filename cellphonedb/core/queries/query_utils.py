import pandas as pd


def merge_cellphone_genes(cluster_counts: pd.DataFrame, genes_expanded: pd.DataFrame) -> pd.DataFrame:
    """
    Merges cluster genes with CellPhoneDB values
    """

    multidata_counts = pd.merge(cluster_counts, genes_expanded, left_index=True, right_on='ensembl')

    return multidata_counts


def get_counts_proteins_of_complexes(cluster_counts: pd.DataFrame, multidatas: pd.DataFrame,
                                     complex_composition):
    cluster_clean = cluster_counts.drop(complex_composition.columns.values, errors='ignore', axis=1)

    complex_components_data = pd.merge(multidatas, complex_composition, left_on='id_multidata',
                                       right_on='complex_multidata_id')

    complex_components_data = pd.merge(complex_components_data, cluster_clean, left_on='protein_multidata_id',
                                       right_on='id_multidata', suffixes=['_complex', ''])

    complex_components_data.rename(columns={'name_complex': 'complex_name'}, index=str, inplace=True)

    if complex_components_data.empty:
        return pd.DataFrame()

    result_receptor_complex = complex_components_data.assign(is_complex=True)
    return result_receptor_complex
