import pandas as pd


def can_be_receptor(multidata: pd.Series, suffix: str = '') -> bool:
    if multidata['receptor{}'.format(suffix)] and \
            not multidata['other{}'.format(suffix)]:
        return True
    return False


def can_be_ligand(multidata: pd.Series, suffix: str = '') -> bool:
    if multidata['secreted_highlight{}'.format(suffix)]:
        return True
    return False
