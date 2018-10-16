import pandas as pd
import re


def autocomplete_query(genes: pd.DataFrame, multidatas: pd.DataFrame, partial_element: pd.DataFrame) -> pd.DataFrame:
    values = genes[genes['ensembl'].str.contains(partial_element, flags=re.IGNORECASE)]['ensembl']
    values = values.append(
        genes[genes['entry_name'].str.contains(partial_element, flags=re.IGNORECASE)]['entry_name'],
        ignore_index=True)
    values = values.append(
        genes[genes['gene_name'].str.contains(partial_element, flags=re.IGNORECASE)]['gene_name'],
        ignore_index=True)
    values = values.append(
        multidatas[multidatas['name'].str.contains(partial_element, flags=re.IGNORECASE)]['name'],
        ignore_index=True)
    result = pd.DataFrame(data=values, columns=['value'])

    return result
