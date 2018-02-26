import pandas as pd

from utilities import dataframe_format


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


def is_receptor_ligand(interaction: pd.Series, receptor_suffix: str, ligand_suffix: str,
                       score_two_suffix: str = '_2') -> bool:
    """
    :param interaction:
    :param receptor_suffix: usually _1 or _2
    :param ligand_suffix: usually _1 or _2
    :return:
    """
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


def get_receptor_ligand_ligand_receptor(interactions: pd.DataFrame) -> pd.DataFrame:
    """
    return a table of receptor ligand interactons
    """
    interactions = interactions.rename(index=str, columns={'score_1': 'score_one', 'score_2': 'score_two'})

    interactions_enabled_rl = interactions[
        interactions.apply(lambda interaction: is_receptor_ligand(interaction, '_1', '_2', '_two'), axis=1)]
    interactions_enabled_rl = dataframe_format.change_column_suffix(interactions_enabled_rl, '_1', '_receptor')
    interactions_enabled_rl = dataframe_format.change_column_suffix(interactions_enabled_rl, '_2', '_ligand')

    interactions_enabled_lr = interactions[
        interactions.apply(lambda interaction: is_receptor_ligand(interaction, '_2', '_1', '_two'), axis=1)].copy()
    interactions_enabled_lr = dataframe_format.change_column_suffix(interactions_enabled_lr, '_2', '_receptor')
    interactions_enabled_lr = dataframe_format.change_column_suffix(interactions_enabled_lr, '_1', '_ligand')

    interactions_enabled = interactions_enabled_rl.append(interactions_enabled_lr)

    interactions_enabled = interactions_enabled.rename(index=str,
                                                       columns={'score_one': 'score_1', 'score_two': 'score_2'})
    interactions_enabled.drop_duplicates(['id_multidata_receptor', 'id_multidata_ligand'], inplace=True)
    interactions_enabled.drop_duplicates(['id_interaction'], inplace=True)
    interactions_enabled.reset_index(drop=True, inplace=True)

    return interactions_enabled
