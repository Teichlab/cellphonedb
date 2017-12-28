from cellphonedb.models.multidata.properties_multidata import is_ligand


def is_receptor_ligand_by_receptor(interaction, receptor):
    """

    :type interaction:
    :type receptor:
    :rtype:
    """
    if interaction['multidata_1_id'] == receptor['id_multidata'] \
            and interaction['is_cellphone_ligand_2']:
        return True

    if interaction['multidata_2_id'] == receptor['id_multidata'] \
            and interaction['is_cellphone_ligand_1']:
        return True

    return False
