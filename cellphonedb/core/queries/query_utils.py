import pandas as pd


def merge_cellphone_genes(cluster_counts: pd.DataFrame, genes_expanded: pd.DataFrame) -> pd.DataFrame:
    """
    Merges cluster genes with CellPhoneDB values
    """

    multidata_counts = pd.merge(cluster_counts, genes_expanded, left_index=True, right_on='ensembl')

    return multidata_counts


def get_counts_proteins_of_complexes(cluster_counts, clusters_names, interactions, suffix, complex_composition):
    receptor_complex_interactions = interactions.loc[interactions['is_complex%s' % suffix] == True]
    receptor_complex_interactions = pd.merge(receptor_complex_interactions, complex_composition,
                                             left_on='id_multidata%s' % suffix, right_on='complex_multidata_id')
    receptor_complex_interactions = pd.merge(receptor_complex_interactions, cluster_counts,
                                             left_on='protein_multidata_id', right_on='id_multidata')

    if receptor_complex_interactions.empty:
        return pd.DataFrame()
    result_receptor_complex = receptor_complex_interactions[
        ['id_interaction', 'entry_name', 'name', 'gene_name', 'name%s' % suffix] + list(clusters_names)]
    result_receptor_complex = result_receptor_complex.rename(columns={'name%s' % suffix: 'complex_name'}, index=str)
    result_receptor_complex = result_receptor_complex.assign(is_complex=True)
    return result_receptor_complex
