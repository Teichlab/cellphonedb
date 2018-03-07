import pandas as pd


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
