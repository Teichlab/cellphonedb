def is_receptor(multidata, suffix=''):
    """

    :type multidata: pd.Series
    :rtype: bool
    """
    if multidata['receptor%s' % suffix] and multidata['transmembrane%s' % suffix]:
        return True

    return False


def is_ligand(multidata, suffix=''):
    """

    :type multidata: pd.Series
    :type is_ligand: str
    :rtype: bool
    """

    if multidata['secretion%s' % suffix] == True \
            and multidata['other%s' % suffix] == False:
        return True

    if multidata['transmembrane%s' % suffix] == True \
            and multidata['secretion%s' % suffix] == False \
            and multidata['extracellular%s' % suffix] == True \
            and multidata['cytoplasm%s' % suffix] == False \
            and multidata['other%s' % suffix] == False \
            and multidata['transporter%s' % suffix] == False:
        return True

    return False
