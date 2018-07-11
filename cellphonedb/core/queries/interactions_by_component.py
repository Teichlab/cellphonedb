import pandas as pd


def call(input: str, interactions: pd.DataFrame) -> pd.DataFrame:
    interactions_filtered = interactions[(interactions['name_1'] == input) |
                                         (interactions['name_2'] == input) |
                                         (interactions['gene_name_1'] == input) |
                                         (interactions['gene_name_2'] == input) |
                                         (interactions['ensembl_1'] == input) |
                                         (interactions['ensembl_2'] == input)]

    def simple_complex_indicator(interaction: pd.Series, suffix: str) -> str:
        if interaction['is_complex{}'.format(suffix)]:
            return 'complex:{}'.format(interaction['name{}'.format(suffix)])

        return 'simple:{}'.format(interaction['name{}'.format(suffix)])

    interactions_filtered['partner_a'] = interactions_filtered.apply(
        lambda interaction: simple_complex_indicator(interaction, '_1'), axis=1)
    interactions_filtered['partner_b'] = interactions_filtered.apply(
        lambda interaction: simple_complex_indicator(interaction, '_2'), axis=1)

    interactions_filtered = interactions_filtered[
        ['id_cp_interaction', 'partner_a', 'partner_b', 'ensembl_1', 'ensembl_2', 'is_complex_1', 'is_complex_2',
         'stoichiometry_1', 'stoichiometry_2', 'source']]

    interactions_filtered.rename(
        columns={'ensembl_1': 'ensembl_a', 'ensembl_2': 'ensembl_b',
                 'stoichiometry_1': 'stoichiometry_a', 'stoichiometry_2': 'stoichiometry_b',
                 'is_complex_1': 'is_complex_a', 'is_complex_2': 'is_complex_b'},
        inplace=True)

    return interactions_filtered
