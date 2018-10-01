import pandas as pd

from cellphonedb.src.core.utils.filters import remove_not_defined_columns


def _only_uniprots_in_df(uniprots_df, inweb_interactions):
    inweb_cellphone = pd.merge(inweb_interactions, uniprots_df, left_on=['protein_1'],
                               right_on=['uniprot'], how='inner')

    remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)

    inweb_cellphone = pd.merge(inweb_cellphone, uniprots_df, left_on=['protein_2'],
                               right_on=['uniprot'], how='inner')
    remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)

    # Prevents duplicated interactions if any uniprot is duplicated in uniprots_df or intaractions
    inweb_cellphone = inweb_cellphone[inweb_cellphone.duplicated() == False]

    return remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)


def _only_genes_in_df(genes_df, interactions):
    result = pd.merge(interactions, genes_df, left_on=['gene_1'],
                      right_on=['ensembl'], how='inner')

    result = pd.merge(result, genes_df, left_on=['gene_2'],
                      right_on=['ensembl'], how='inner', suffixes=['_1', '_2'])

    # Prevents duplicated interactions if any uniprot is duplicated in uniprots_df or intaractions
    result = result[result.duplicated() == False]

    return result
