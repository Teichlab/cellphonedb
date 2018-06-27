import pandas as pd

from tools import app
from tools.generate_data.filters import remove_genes
from utils import utils


def generate_genes_action(gene_base_filename: str, remove_genes_filename: str):
    gene_base_filename = '{}/{}'.format(app.data_dir, gene_base_filename)
    remove_genes_filename = '{}/{}'.format(app.data_dir, remove_genes_filename)

    gene_base_data = utils.read_data_table_from_file(gene_base_filename)
    remove_genes_data = utils.read_data_table_from_file(remove_genes_filename)

    genes_filtered = remove_genes.remove_genes_in_file(gene_base_data, remove_genes_data)

    genes_filtered.to_csv('{}/{}'.format(app.output_dir, 'gene_filtered.csv'), index=False)


def generate_genes_from_uniprot_ensembl_db(uniprot_db_filename: str, ensembl_db_filename: str, proteins_filename: str):
    uniprot_db_filename = '{}/{}'.format(app.data_dir, uniprot_db_filename)
    ensembl_db_filename = '{}/{}'.format(app.data_dir, ensembl_db_filename)
    proteins_filename = '{}/{}'.format(app.data_dir, proteins_filename)

    uniprots = utils.read_data_table_from_file(uniprot_db_filename)
    ensembls = utils.read_data_table_from_file(ensembl_db_filename)
    proteins = utils.read_data_table_from_file(proteins_filename)

    uniprots_merged = pd.merge(proteins, uniprots, left_on='uniprot', right_on='Entry', indicator=True, how='outer')

    only_in_protein = uniprots_merged[uniprots_merged['_merge'] == 'left_only']

    if not only_in_protein.empty:
        print('SOME PROTEINS DIDNT EXIST IN UNIPROT DATABASE')
        print(only_in_protein['uniprot'].tolist())

    uniprots_filtered = uniprots_merged[uniprots_merged['_merge'] == 'both']

    uniprots_filtered = _deconvolute_genenames(uniprots_filtered)

    print(uniprots_filtered.columns.values)

    merged_genes = pd.merge(uniprots_filtered, ensembls, left_on=0, right_on='Gene name')

    merged_from_uniprot = pd.DataFrame()
    merged_from_uniprot[['ensembl', 'uniprot', 'gene_name', 'hgnc_symbol']] = merged_genes[
        ['Gene stable ID', 'Entry', 'Gene name', 'HGNC symbol']]

    merged_from_ensembl = pd.DataFrame()
    merged_from_ensembl[['ensembl', 'uniprot', 'gene_name', 'hgnc_symbol']] = merged_genes[[
        'Gene stable ID', 'UniProtKB/Swiss-Prot ID', 'Gene name', 'HGNC symbol']]

    result = merged_from_uniprot.append(merged_from_ensembl, sort=False).reset_index(drop=True)

    result.dropna(subset=['ensembl', 'uniprot', 'gene_name'], inplace=True)

    print(result[pd.isnull(result['hgnc_symbol'])].drop_duplicates().to_csv(index=False))

    result = result.drop_duplicates().reset_index(drop=True)

    result = result[~result['gene_name'].str.contains('HLA')]

    result = result[result['uniprot'].apply(lambda uniprot: uniprot in proteins['uniprot'].tolist())]

    result = result.sort_values(by=list(result.columns.values))

    assert len(result) == 6272
    result.to_csv('TEST_GENE_RESULT.csv', index=False)


def _deconvolute_genenames(uniprots_filtered):
    uniprots_columns = ['Entry', 'Gene names', 'Ensembl transcript']
    uniprots_filtered = uniprots_filtered[uniprots_columns]
    deconvoluted = uniprots_filtered['Gene names'].str.split(' ').apply(pd.Series)
    deconvoluted.index = uniprots_filtered.set_index(uniprots_columns).index
    deconvoluted = deconvoluted.stack().reset_index(uniprots_columns).reset_index(drop=True)
    return deconvoluted
#
