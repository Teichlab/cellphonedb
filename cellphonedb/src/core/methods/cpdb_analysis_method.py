import pandas as pd

from cellphonedb.src.core.exceptions.EmptyResultException import EmptyResultException
from cellphonedb.src.core.exceptions.NoComplexException import NoComplexException
from cellphonedb.src.core.methods import cpdb_analysis_simple_method, cpdb_analysis_complex_method


def call(meta: pd.DataFrame,
         counts: pd.DataFrame,
         counts_data: str,
         interactions: pd.DataFrame,
         genes: pd.DataFrame,
         complexes: pd.DataFrame,
         complex_compositions: pd.DataFrame,
         separator: str,
         threshold: float = 0.1,
         result_precision: int = 3) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    means_simple, significant_means_simple, deconvoluted_simple = \
        cpdb_analysis_simple_method.call(meta.copy(),
                                         counts.copy(),
                                         counts_data,
                                         interactions.copy(),
                                         separator,
                                         threshold,
                                         result_precision)

    try:
        means_complex, significant_means_complex, deconvoluted_complex = \
            cpdb_analysis_complex_method.call(meta.copy(),
                                              counts.copy(),
                                              counts_data,
                                              interactions.copy(),
                                              genes,
                                              complexes,
                                              complex_compositions,
                                              separator,
                                              threshold,
                                              result_precision)
        means = means_simple.append(means_complex, sort=False)
        significant_means = significant_means_simple.append(significant_means_complex, sort=False)
        deconvoluted = deconvoluted_simple.append(deconvoluted_complex, sort=False)

    except NoComplexException:
        means = means_simple
        significant_means = significant_means_simple
        deconvoluted = deconvoluted_simple

    deconvoluted.drop_duplicates(inplace=True)

    if means.empty:
        raise EmptyResultException

    max_rank = significant_means['rank'].max()
    significant_means['rank'] = significant_means['rank'].apply(lambda rank: rank if rank != 0 else (1 + max_rank))
    significant_means.sort_values('rank', inplace=True)

    return means, significant_means, deconvoluted
