import pandas as pd


def gene_generator(ensembl_db: pd.DataFrame,
                   uniprot_db: pd.DataFrame,
                   hla_genes: pd.DataFrame,
                   interactions: pd.DataFrame,
                   result_columns: list) -> pd.DataFrame:
    def get_first_gene_name(gene_names: str) -> str:
        if type(gene_names) != str:
            return ''
        gene_names = gene_names.split(' ')

        return gene_names[0]

    uniprot_db = uniprot_db.copy()
    uniprot_db['gene_name'] = uniprot_db['gene_names'].apply(get_first_gene_name)
    uniprot_db.dropna(inplace=True)
    uniprot_db.drop_duplicates(['gene_name', 'uniprot'], inplace=True)
    interactions_partners = interactions[['partner_a', 'protein_name_a']].append(
        interactions[['partner_b', 'protein_name_b']].rename(
            {'partner_b': 'partner_a', 'protein_name_b': 'protein_name_a'}, axis=1), sort=False)
    interactions_partners_uniprot = interactions_partners.dropna()['partner_a']
    interactions_partners_uniprot = interactions_partners_uniprot.drop_duplicates()

    # Check if all interaction uniprot are in uniprot database (except HLA)
    interaction_partners_not_in_uniprot_database = interactions_partners_uniprot[
        interactions_partners_uniprot.apply(lambda uniprot: uniprot not in uniprot_db['uniprot'].tolist())]
    print('Check if all interactions partners are in uniprot db')
    print(interaction_partners_not_in_uniprot_database)
    cpdb_uniprots = uniprot_db[
        uniprot_db['uniprot'].apply(lambda uniprot: uniprot in interactions_partners_uniprot.tolist())]

    # Remove hla genes
    cpdb_uniprots = cpdb_uniprots[~cpdb_uniprots['gene_name'].str.contains('HLA')]

    # Merge with ensembl database
    cpdb_genes = cpdb_uniprots.merge(ensembl_db, how='inner', on='gene_name', sort=False).drop_duplicates(
        ['uniprot', 'gene_name'])
    print('Missing interactions afger uniprotdb merge')
    print(interaction_partners_not_in_uniprot_database)

    # Check if all cpdb uniprots are in the cpdb_genes after merge with ensembl
    genes_missing_after_ensembl_merge = cpdb_uniprots[
        cpdb_uniprots['uniprot'].apply(lambda uniprot: uniprot not in cpdb_genes['uniprot'].tolist())]
    print('Missing uniprots after merge')
    print(genes_missing_after_ensembl_merge)

    # Check if all interaction uniprot are in uniprot database
    interaction_partners_not_in_uniprot_database = interactions_partners_uniprot[
        interactions_partners_uniprot.apply(lambda uniprot: uniprot not in cpdb_genes['uniprot'].tolist())]
    print('Proteins without Gene')
    print(interaction_partners_not_in_uniprot_database)

    # Get missing genes from ensembl using uniprot
    genes_missing_after_ensembl_merge = genes_missing_after_ensembl_merge.merge(
        ensembl_db,
        how='inner',
        left_on='uniprot',
        right_on='uniprot_ensembl',
        suffixes=('_uniprot', '_ensembl'),
        sort=False,
    ).drop_duplicates(['uniprot', 'uniprot_ensembl'])
    genes_missing_after_ensembl_merge.rename({'gene_name_ensembl': 'gene_name'}, axis=1, inplace=True)

    # Merging missing cpdb_uniprot_genes and missing uniprot_genes
    cpdb_genes = cpdb_genes.append(genes_missing_after_ensembl_merge, ignore_index=True, sort=False)[result_columns]
    cpdb_genes = cpdb_genes.append(hla_genes, ignore_index=True, sort=False).drop_duplicates(result_columns)

    # Check if exist any duplicated ensembl
    print('Duplicated ensembl genes')
    print(cpdb_genes[cpdb_genes['ensembl'].duplicated()])

    # Check if all interaction uniprot are in uniprot database
    interaction_partners_not_in_uniprot_database = interactions_partners_uniprot[
        interactions_partners_uniprot.apply(lambda uniprot: uniprot not in cpdb_genes['uniprot'].tolist())]
    print('Proteins without Gene')
    print(interaction_partners_not_in_uniprot_database)

    return cpdb_genes[result_columns]
