import pandas as pd

from cellphonedb.core.core_logger import core_logger
from cellphonedb.core.database import DatabaseManager
from cellphonedb.core.methods import cluster_statistical_analysis_simple, \
    cluster_statistical_analysis_complex


class MethodLauncher():
    def __init__(self, database_manager: DatabaseManager, default_threads: int):
        self.database_manager = database_manager
        self.default_threads = default_threads

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Launching Method {}'.format(name))

        return method

    def get_multidatas_from_string(self, string: str) -> pd.DataFrame:
        multidatas = self.database_manager.get_repository('multidata').get_multidatas_from_string(string)
        return multidatas

    def cluster_statistical_analysis(self, meta: pd.DataFrame, count: pd.DataFrame, iterations: int, threshold: float,
                                     threads: int, debug_seed: int) -> (
            pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):

        if threads < 1:
            core_logger.info('Using Default thread number: %s' % self.default_threads)
            threads = self.default_threads

        pvalues_simple, means_simple, significant_means_simple, mean_pvalue_simple, deconvoluted_simple = self.cluster_statistical_analysis_simple(
            meta, count, iterations, threshold, threads, debug_seed)
        pvalues_complex, means_complex, significant_means_complex, mean_pvalue_complex, deconvoluted_complex = self.cluster_statistical_analysis_complex(
            meta, count, iterations, threshold, threads, debug_seed)

        pvalues = pvalues_simple.append(pvalues_complex, sort=False)
        means = means_simple.append(means_complex, sort=False)
        significant_means = significant_means_simple.append(significant_means_complex, sort=False)
        mean_pvalue = mean_pvalue_simple.append(mean_pvalue_complex, sort=False)
        deconvoluted = deconvoluted_simple.append(deconvoluted_complex, sort=False)
        if not 'complex_name' in deconvoluted:
            deconvoluted['complex_name'] = ''

        return pvalues, means, significant_means, mean_pvalue, deconvoluted

    def cluster_statistical_analysis_simple(self, meta: pd.DataFrame, count: pd.DataFrame, iterations: int,
                                            threshold: float, threads: int, debug_seed: int) -> (
            pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()

        return cluster_statistical_analysis_simple.call(meta, count, interactions, iterations, threshold, threads,
                                                        debug_seed)

    def cluster_statistical_analysis_complex(self, meta: pd.DataFrame, count: pd.DataFrame, iterations: int,
                                             threshold: float, threads: int, debug_seed: int) -> (
            pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
        interactions = self.database_manager.get_repository('interaction').get_all_expanded()
        genes = self.database_manager.get_repository('gene').get_all_expanded()
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()

        return cluster_statistical_analysis_complex.call(meta, count, interactions, genes, complex_expanded,
                                                         complex_composition, iterations, threshold, threads,
                                                         debug_seed)
