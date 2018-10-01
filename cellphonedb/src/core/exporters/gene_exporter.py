from cellphonedb.src.core.utils import filters


def call(gene_expanded, output_columns):
    filters.remove_not_defined_columns(gene_expanded, output_columns)

    gene_expanded.drop(['id_gene', 'protein_id'], axis=1, inplace=True)

    gene_expanded.rename(index=str, columns={'name': 'uniprot'}, inplace=True)
    return gene_expanded
