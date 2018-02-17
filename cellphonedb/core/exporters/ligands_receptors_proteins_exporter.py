from cellphonedb.models.multidata import filters_multidata


def call(genes_expanded):
    genes_expanded_filtered = filters_multidata.filter_by_lingand_or_receptor(genes_expanded)
    result = genes_expanded_filtered.loc[:, [
                                                'ensembl', 'name', 'entry_name', 'transmembrane', 'secretion',
                                                'peripheral',
                                                'is_cellphone_receptor', 'is_cellphone_ligand', 'transporter', 'other',
                                                'other_desc',
                                                'tags', 'tags_reason', 'cytoplasm', 'extracellular']]

    result.rename(columns={'name': 'uniprot', 'secretion': 'secreted', 'peripheral': 'peripheral_proteins',
                           'is_cellphone_receptor': 'receptor_cellphone', 'is_cellphone_ligand': 'ligands_cellphone'},
                  inplace=True)

    return result
