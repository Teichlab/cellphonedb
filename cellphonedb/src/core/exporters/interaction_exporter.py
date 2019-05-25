import pandas as pd


def call(interactions_expanded: pd.DataFrame) -> pd.DataFrame:
    interactions_expanded = interactions_expanded[interactions_expanded['is_cellphonedb_interactor']].copy()
    interactions_expanded.rename(index=str, columns={'name_1': 'partner_a', 'name_2': 'partner_b'},
                                 inplace=True)

    return interactions_expanded[
        ['id_cp_interaction', 'partner_a', 'partner_b', 'protein_name_1', 'protein_name_2', 'source',
         'comments_interaction', 'iuphar']]
