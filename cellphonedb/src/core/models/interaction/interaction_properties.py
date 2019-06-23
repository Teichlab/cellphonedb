import pandas as pd

from cellphonedb.src.core.models.multidata import multidata_properties


def is_cellphonedb_interactor(interaction: pd.Series, suffixes=('_1', '_2')) -> bool:
    if interaction['annotation_strategy'] == 'curated':
        return True

    if interaction['annotation_strategy'] == 'user_curated':
        return True

    if interaction['id_multidata{}'.format(suffixes[0])] == interaction['id_multidata{}'.format(suffixes[1])]:
        return False

    if interaction['annotation_strategy'] == 'guidetopharmacology.org':
        return True

    if multidata_properties.can_be_receptor(interaction, suffixes[0]) and \
            multidata_properties.can_be_ligand(interaction, suffixes[1]):
        return True

    if multidata_properties.can_be_receptor(interaction, suffixes[1]) and \
            multidata_properties.can_be_ligand(interaction, suffixes[0]):
        return True

    return False
