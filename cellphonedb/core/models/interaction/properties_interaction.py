import pandas as pd


# TODO: Remove me
def is_receptor_ligand_by_receptor(interaction: pd.Series, receptor: pd.Series) -> bool:
    if interaction['multidata_1_id'] == receptor['id_multidata'] \
            and interaction['is_cellphone_ligand_2']:
        return True

    if interaction['multidata_2_id'] == receptor['id_multidata'] \
            and interaction['is_cellphone_ligand_1']:
        return True

    return False


# TODO: Remove me
def is_receptor_ligand_or_ligand_receptor(interaction: pd.DataFrame, suffix: list = ['_1', '_2']) -> bool:
    if interaction['is_cellphone_receptor{}'.format(suffix[0])] and interaction[
        'is_cellphone_ligand{}'.format(suffix[1])]:
        return True

    if interaction['is_cellphone_receptor{}'.format(suffix[1])] and interaction[
        'is_cellphone_ligand{}'.format(suffix[0])]:
        return True

    return False


def is_receptor_ligand(interaction: pd.Series, enable_integrin: bool, receptor_suffix: str, ligand_suffix: str,
                       score_two_suffix: str = '_2') -> bool:
    """
    :param interaction:
    :param receptor_suffix: usually _1 or _2
    :param ligand_suffix: usually _1 or _2
    :return:
    """
    if enable_integrin:
        if interaction['integrin_interaction{}'.format(receptor_suffix)]:
            return True

    if not interaction['is_cellphone_receptor{}'.format(receptor_suffix)]:
        return False

    if interaction['source'] == 'curated':
        return True

    if (interaction['secreted_highlight{}'.format(ligand_suffix)]) & (
            interaction['score{}'.format(score_two_suffix)] >= 0.3):
        return True

    return False
