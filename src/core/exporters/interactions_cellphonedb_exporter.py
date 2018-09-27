import pandas as pd


def call(interactions: pd.DataFrame()) -> pd.DataFrame():
    interactions_filtered = interactions[interactions['is_cellphonedb_interactor']].copy()

    def simple_complex_indicator(interaction: pd.Series, suffix: str) -> str:
        if interaction['is_complex{}'.format(suffix)]:
            return 'complex:{}'.format(interaction['name{}'.format(suffix)])

        return 'simple:{}'.format(interaction['name{}'.format(suffix)])

    interactions_filtered['partner_a'] = interactions.apply(
        lambda interaction: simple_complex_indicator(interaction, '_a'),
        axis=1)
    interactions_filtered['partner_b'] = interactions.apply(
        lambda interaction: simple_complex_indicator(interaction, '_b'),
        axis=1)

    interactions_filtered['secreted'] = (interactions_filtered['secretion_a'] | interactions_filtered['secretion_b'])
    interactions_filtered['is_integrin'] = (
            interactions_filtered['integrin_interaction_a'] | interactions_filtered['integrin_interaction_b'])

    return interactions_filtered[
        ['id_cp_interaction', 'source', 'partner_a', 'partner_b', 'entry_name_a', 'entry_name_b', 'secreted',
         'is_integrin', 'comments_interaction', 'dlrp', 'iuphar']]
