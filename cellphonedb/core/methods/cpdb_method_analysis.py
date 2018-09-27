import pandas as pd

from cellphonedb.core.methods import cpdb_method_analysis_simple, cpdb_method_analysis_complex


def call(meta: pd.DataFrame,
         counts: pd.DataFrame,
         interactions: pd.DataFrame,
         genes: pd.DataFrame,
         complexes: pd.DataFrame,
         complex_compositions: pd.DataFrame,
         threshold: float = 0.1,
         threads: int = 4,
         debug_seed=False,
         round_decimals: int = 1) -> (
        pd.DataFrame, pd.DataFrame):
    means_simple, deconvoluted_simple = cpdb_method_analysis_simple.call(meta.copy(),
                                                                         counts.copy(),
                                                                         interactions.copy(),
                                                                         threshold,
                                                                         threads,
                                                                         debug_seed,
                                                                         round_decimals)
    means_complex, deconvoluted_complex = cpdb_method_analysis_complex.call(meta,
                                                                            counts,
                                                                            interactions,
                                                                            genes,
                                                                            complexes,
                                                                            complex_compositions,
                                                                            threshold,
                                                                            threads,
                                                                            debug_seed,
                                                                            round_decimals)

    means = means_simple.append(means_complex, sort=False)
    deconvoluted = deconvoluted_simple.append(deconvoluted_complex, sort=False)

    if not 'complex_name' in deconvoluted:
        deconvoluted['complex_name'] = ''
    return means, deconvoluted
