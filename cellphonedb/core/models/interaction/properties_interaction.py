import pandas as pd

from cellphonedb.core.models.multidata import properties_multidata


def is_cellphone_interactor(interaction: pd.Series, suffixes=('_1', '_2')) -> bool:
    if interaction['source'] == 'curated':
        return True

    if interaction['iuhpar']:
        return True

    if properties_multidata.can_be_receptor(interaction, suffixes[0]) and \
            properties_multidata.can_be_ligand(interaction, suffixes[1]):
        return True

    if properties_multidata.can_be_receptor(interaction, suffixes[1]) and \
            properties_multidata.can_be_ligand(interaction, suffixes[0]):
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
            interaction['score{}'.format(score_two_suffix)] > 0.3):
        return True

    return False
