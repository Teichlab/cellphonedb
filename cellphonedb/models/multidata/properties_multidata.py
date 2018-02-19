import pandas as pd


def is_receptor(multidata: pd.Series, suffix: str = '') -> bool:
    if multidata['receptor%s' % suffix] and \
            multidata['transmembrane%s' % suffix] and \
            not multidata['other{}'.format(suffix)]:
        return True

    return False


def is_secreted_ligand(multidata: pd.Series, suffix: str = ''):
    if multidata['secreted_highlight{}'.format(suffix)]:
        return True

    return False


def is_transmembrane_ligand(multidata: pd.Series, suffix: str = ''):
    if multidata['transmembrane{}'.format(suffix)]:
        return True
    return False
