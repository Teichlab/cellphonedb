import pandas as pd

from src.core.methods import cpdb_analysis_simple_method, cpdb_analysis_complex_method


def call(meta: pd.DataFrame,
         counts: pd.DataFrame,
         interactions: pd.DataFrame,
         genes: pd.DataFrame,
         complexes: pd.DataFrame,
         complex_compositions: pd.DataFrame,
         threshold: float = 0.1,
         round_decimals: int = 1) -> (
        pd.DataFrame, pd.DataFrame):
    means_simple, deconvoluted_simple = cpdb_analysis_simple_method.call(meta.copy(),
                                                                         counts.copy(),
                                                                         interactions.copy(),
                                                                         threshold,
                                                                         round_decimals)
    means_complex, deconvoluted_complex = cpdb_analysis_complex_method.call(meta,
                                                                            counts,
                                                                            interactions,
                                                                            genes,
                                                                            complexes,
                                                                            complex_compositions,
                                                                            threshold,
                                                                            round_decimals)

    means = means_simple.append(means_complex, sort=False)
    deconvoluted = deconvoluted_simple.append(deconvoluted_complex, sort=False)

    if not 'complex_name' in deconvoluted:
        deconvoluted['complex_name'] = ''
    return means, deconvoluted
