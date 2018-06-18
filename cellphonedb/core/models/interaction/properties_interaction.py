import pandas as pd

from cellphonedb.core.models.multidata import properties_multidata


def is_cellphonedb_interactor(interaction: pd.Series, suffixes=('_1', '_2')) -> bool:
    if interaction['id_multidata{}'.format(suffixes[0])] == interaction['id_multidata{}'.format(suffixes[1])]:
        return False

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
