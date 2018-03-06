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


def is_cellphone_ligand(multidata: pd.Series, interactions_extended: pd.DataFrame) -> bool:
    multidata = multidata.to_frame().transpose()
    receptor_is_2 = pd.merge(multidata, interactions_extended, left_on='id_multidata', right_on='multidata_1_id')

    receptor_is_2 = receptor_is_2[receptor_is_2['is_cellphone_receptor_2']]

    if receptor_is_2[receptor_is_2['source'] == 'curated'].empty == False:
        return True

    if receptor_is_2[(receptor_is_2['score_2'] > 0.3) & (receptor_is_2['secreted_highlight_1'])].empty == False:
        return True

    receptor_is_1 = pd.merge(multidata, interactions_extended, left_on='id_multidata', right_on='multidata_2_id')
    receptor_is_1 = receptor_is_1[receptor_is_1['is_cellphone_receptor_1']]

    if receptor_is_1[receptor_is_1['source'] == 'curated'].empty == False:
        return True

    if receptor_is_1[(receptor_is_1['secreted_highlight_2']) & (receptor_is_1['score_2'] > 0.3)].empty == False:
        return True

    return False
