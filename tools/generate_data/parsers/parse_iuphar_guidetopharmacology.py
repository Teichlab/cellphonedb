import pandas as pd


def call(iuphar_guidepharmacology: pd.DataFrame, genes: pd.DataFrame, proteins: pd.DataFrame) -> pd.DataFrame:
    iuphar_filtered = iuphar_guidepharmacology[iuphar_guidepharmacology['target_species'] == 'Human']

    iuphar_filtered = iuphar_filtered[iuphar_filtered['ligand_species'] == 'Human']

    iuphar_filtered.dropna(subset=['target_uniprot'], inplace=True)

    iuphar_filtered = iuphar_filtered[iuphar_filtered['target_uniprot'].apply(lambda uniprot: '|' not in uniprot)]

    missing_uniprots = iuphar_filtered[~iuphar_filtered['target_uniprot'].isin(proteins['uniprot'])][
        'target_uniprot'].drop_duplicates()

    if not missing_uniprots.empty:
        print('WARNING: {} UNIPROTS IN GUIDETOPHARMACOLOGY DATABASE DIDNT EXIST IN CELLPHONEDB DATABASE'.format(
            len(missing_uniprots)))
        print(missing_uniprots.tolist())

    iuphar_filtered = iuphar_filtered[iuphar_filtered['target_uniprot'].isin(proteins['uniprot'])]

    iuphar_filtered.dropna(subset=['ligand_gene_symbol'], inplace=True)
    missing_genes = iuphar_filtered[~iuphar_filtered['ligand_gene_symbol'].isin(genes['gene_name'])][
        'ligand_gene_symbol'].drop_duplicates()

    if not missing_genes.empty:
        print('WARNING: {} GENE NAMES IN GUIDETOPHARMACOLOGY DATABASE DIDNT EXIST IN CELLPHONEDB DATABASE'.format(
            len(missing_genes)))
        print(missing_genes.tolist())

    iuphar_filtered = pd.merge(iuphar_filtered, genes, left_on='ligand_gene_symbol', right_on='gene_name')
    iuphar_filtered_cellphone_format = pd.DataFrame()
    iuphar_filtered_cellphone_format[['uniprot_1', 'uniprot_2']] = iuphar_filtered[
        ['uniprot', 'target_uniprot']]

    iuphar_filtered_cellphone_format['source'] = 'guidetopharmacology.org'
    iuphar_filtered_cellphone_format['iuphar'] = True

    iuphar_filtered_cellphone_format.drop_duplicates(inplace=True)

    return iuphar_filtered_cellphone_format
