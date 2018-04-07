import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction


def call(interactions: pd.DataFrame) -> pd.DataFrame:
    # Necessary to edit suffixes
    interactions_enabled = filter_interaction.filter_by_receptor_ligand_ligand_receptor(
        interactions, enable_integrin=True)

    interactions_enabled['receptor'] = interactions_enabled['entry_name_receptor'].apply(
        lambda value: 'single:%s' % value)

    interactions_enabled.loc[interactions_enabled['is_complex_receptor'], ['receptor']] = \
        interactions_enabled['name_receptor'].apply(lambda value: 'complex:%s' % value)

    interactions_enabled['ligand'] = interactions_enabled['entry_name_ligand'].apply(lambda value: 'single:%s' % value)
    interactions_enabled.loc[interactions_enabled['is_complex_ligand'], ['ligand']] = interactions_enabled[
        'name_ligand'].apply(
        lambda value: 'complex:%s' % value)

    interactions_enabled['uniprot_receptor'] = \
        interactions_enabled[interactions_enabled['is_complex_receptor'] == False]['name_receptor']
    interactions_enabled['uniprot_ligand'] = interactions_enabled[interactions_enabled['is_complex_ligand'] == False][
        'name_ligand']

    return interactions_enabled[
        ['id_interaction', 'source', 'score_1', 'score_2', 'receptor', 'ligand', 'uniprot_receptor', 'uniprot_ligand',
         'secreted_desc_receptor', 'secreted_highlight_ligand', 'secreted_desc_ligand', 'comments_interaction']]
