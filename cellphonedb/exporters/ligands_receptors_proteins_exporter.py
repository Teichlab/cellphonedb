from cellphonedb.models.multidata import filters_multidata
from cellphonedb.repository import gene_repository


def call():
    multidatas = gene_repository.get_all_expanded()
    multidatas = filters_multidata.filter_by_lingand_or_receptor(multidatas)
    result = multidatas.loc[:, [
                                   'ensembl', 'name', 'entry_name', 'transmembrane', 'secretion', 'peripheral',
                                   'is_cellphone_receptor', 'is_cellphone_ligand', 'transporter', 'other', 'other_desc',
                                   'tags', 'tags_reason', 'cytoplasm', 'extracellular']]

    result.rename(columns={'name': 'uniprot', 'secretion': 'secreted', 'peripheral': 'peripheral_proteins',
                           'is_cellphone_receptor': 'receptor_cellphone', 'is_cellphone_ligand': 'ligands_cellphone'},
                  inplace=True)

    return result
