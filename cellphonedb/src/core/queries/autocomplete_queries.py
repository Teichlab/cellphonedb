import re

import pandas as pd


def autocomplete_query(genes: pd.DataFrame, multidatas: pd.DataFrame, partial_element: pd.DataFrame) -> pd.DataFrame:
    values = _partial_filter(genes, 'ensembl', partial_element)

    by_protein_name = _partial_filter(genes, 'protein_name', partial_element)
    by_gene_name = _partial_filter(genes, 'gene_name', partial_element)

    with_hgnc_symbol = genes.dropna(subset=['hgnc_symbol'])
    by_hgnc_symbol = _partial_filter(with_hgnc_symbol, 'hgnc_symbol', partial_element)

    by_name = _partial_filter(multidatas, 'name', partial_element)

    values = values.append(by_protein_name, ignore_index=True)
    values = values.append(by_gene_name, ignore_index=True)
    values = values.append(by_hgnc_symbol, ignore_index=True)
    values = values.append(by_name, ignore_index=True)

    result = pd.DataFrame(data=values, columns=['value']).drop_duplicates()

    return result


def _partial_filter(input_data, name, partial_element):
    matching = input_data[input_data[name].str.contains(partial_element, flags=re.IGNORECASE)][name]
    return matching
