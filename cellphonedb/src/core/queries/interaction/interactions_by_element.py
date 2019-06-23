from functools import reduce
from typing import List

import pandas as pd


def call(element: str, interactions: pd.DataFrame, complex_composition: pd.DataFrame) -> pd.DataFrame:
    elements = [name.strip() for name in element.split(',')]
    related_complexes = _find_complex_by_elements(elements, complex_composition)

    elements = elements + related_complexes

    interactions_filtered = pd.DataFrame()

    interactions_filtered = _find_interactions_by_elements(elements, interactions, interactions_filtered)

    if interactions_filtered.empty:
        return interactions_filtered

    interactions_filtered = _build_result(interactions_filtered)

    return interactions_filtered.drop_duplicates()


def _build_result(interactions: pd.DataFrame) -> pd.DataFrame:
    def simple_complex_indicator(interaction: pd.Series, suffix: str) -> str:
        if interaction['is_complex{}'.format(suffix)]:
            return 'complex:{}'.format(interaction['name{}'.format(suffix)])

        return 'simple:{}'.format(interaction['name{}'.format(suffix)])

    interactions['partner_a'] = interactions.apply(
        lambda interaction: simple_complex_indicator(interaction, '_a'), axis=1)
    interactions['partner_b'] = interactions.apply(
        lambda interaction: simple_complex_indicator(interaction, '_b'), axis=1)

    interactions = interactions[
        ['id_cp_interaction', 'partner_a', 'partner_b', 'gene_name_a', 'gene_name_b', 'ensembl_a', 'ensembl_b',
         'annotation_strategy']]
    return interactions


def _find_interactions_by_elements(elements: list, interactions: pd.DataFrame,
                                   interactions_filtered: pd.DataFrame) -> pd.DataFrame:
    for element in elements:
        element_interactions = interactions[(interactions['name_a'] == element) |
                                            (interactions['name_b'] == element) |
                                            (interactions['gene_name_a'] == element) |
                                            (interactions['gene_name_b'] == element) |
                                            (interactions['protein_name_a'] == element) |
                                            (interactions['protein_name_b'] == element) |
                                            (interactions['ensembl_a'] == element) |
                                            (interactions['ensembl_b'] == element)].copy()

        interactions_filtered = interactions_filtered.append(element_interactions)

    return interactions_filtered


def _find_complex_by_elements(elements: List[str], complex_composition: pd.DataFrame) -> List[str]:
    all_results = [_find_complex_by_element(element, complex_composition) for element in elements]

    return list(set(reduce((lambda carry, current: carry + current), all_results)))


def _find_complex_by_element(element: str, complex_composition: pd.DataFrame) -> List[str]:
    complexes_filtered = complex_composition[
        (complex_composition['name_protein'] == element) |
        (complex_composition['gene_name_protein'] == element) |
        (complex_composition['protein_name_protein'] == element) |
        (complex_composition['ensembl_protein'] == element)]

    return complexes_filtered['name_complex'].drop_duplicates().tolist()
