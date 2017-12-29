import pandas as pd


def is_receptor_ligand_by_receptor(interaction: pd.Series, receptor: pd.Series) -> bool:
    if interaction['multidata_1_id'] == receptor['id_multidata'] \
            and interaction['is_cellphone_ligand_2']:
        return True

    if interaction['multidata_2_id'] == receptor['id_multidata'] \
            and interaction['is_cellphone_ligand_1']:
        return True

    return False


def is_receptor_ligand_or_ligand_receptor(interaction: pd.DataFrame, suffix: list = ['_1', '_2']) -> bool:
    if interaction['is_cellphone_receptor{}'.format(suffix[0])] and interaction[
        'is_cellphone_ligand{}'.format(suffix[1])]:
        return True

    if interaction['is_cellphone_receptor{}'.format(suffix[1])] and interaction[
        'is_cellphone_ligand{}'.format(suffix[0])]:
        return True

    return False
