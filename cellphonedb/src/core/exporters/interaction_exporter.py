import pandas as pd


def call(interactions_expanded: pd.DataFrame) -> pd.DataFrame:
    interactions_expanded.rename(index=str, columns={'name_1': 'partner_a',
                                                     'name_2': 'partner_b',
                                                     'protein_name_1': 'protein_name_a',
                                                     'protein_name_2': 'protein_name_b'},
                                 inplace=True)

    interactions_expanded.sort_values('id_cp_interaction', inplace=True)
    return interactions_expanded[
        ['id_cp_interaction', 'partner_a', 'partner_b', 'protein_name_a', 'protein_name_b', 'annotation_strategy',
         'source']]
