import pandas as pd

from cellphonedb.src.core.exceptions.EmptyResultException import EmptyResultException
from cellphonedb.src.core.methods import cpdb_statistical_analysis_simple_method, \
    cpdb_statistical_analysis_complex_method


def call(meta: pd.DataFrame,
         count: pd.DataFrame,
         interactions: pd.DataFrame,
         genes: pd.DataFrame,
         complex_expanded: pd.DataFrame,
         complex_composition: pd.DataFrame,
         iterations: int,
         threshold: float,
         threads: int,
         debug_seed: int,
         result_precision: int
         ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    pvalues_simple, means_simple, significant_means_simple, mean_pvalue_simple, deconvoluted_simple = \
        cpdb_statistical_analysis_simple_method.call(meta.copy(),
                                                     count.copy(),
                                                     interactions,
                                                     iterations,
                                                     threshold,
                                                     threads,
                                                     debug_seed,
                                                     result_precision)

    pvalues_complex, means_complex, significant_means_complex, mean_pvalue_complex, deconvoluted_complex = \
        cpdb_statistical_analysis_complex_method.call(meta.copy(),
                                                      count.copy(),
                                                      interactions,
                                                      genes,
                                                      complex_expanded,
                                                      complex_composition,
                                                      iterations,
                                                      threshold,
                                                      threads,
                                                      debug_seed,
                                                      result_precision)

    pvalues = pvalues_simple.append(pvalues_complex, sort=False)
    means = means_simple.append(means_complex, sort=False)
    significant_means = significant_means_simple.append(significant_means_complex, sort=False)

    if means.empty:
        raise EmptyResultException

    max_rank = significant_means['rank'].max()
    significant_means['rank'] = significant_means['rank'].apply(lambda rank: rank if rank != 0 else (1 + max_rank))
    significant_means.sort_values('rank', inplace=True)

    mean_pvalue = mean_pvalue_simple.append(mean_pvalue_complex, sort=False)
    deconvoluted = deconvoluted_simple.append(deconvoluted_complex, sort=False)

    if not 'complex_name' in deconvoluted:
        deconvoluted['complex_name'] = ''

    return deconvoluted, mean_pvalue, means, pvalues, significant_means
