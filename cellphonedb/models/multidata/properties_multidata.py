import pandas as pd


def is_receptor(multidata: pd.Series, suffix: str = '') -> bool:
    if multidata['receptor%s' % suffix] and multidata['transmembrane%s' % suffix]:
        return True

    return False


def is_ligand(multidata: pd.Series, suffix: str = '') -> bool:
    if multidata['secreted_highlight']:
        return True

    if multidata['transmembrane'] and \
            multidata['extracellular'] and \
            not multidata['secreted_highlight'] and \
            not multidata['other'] and \
            not multidata['transporter']:
        return True

    return False
