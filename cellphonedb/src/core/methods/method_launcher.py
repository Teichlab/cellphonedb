import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.database import DatabaseManager
from cellphonedb.src.core.exceptions.ThresholdValueException import ThresholdValueException
from cellphonedb.src.core.methods import cpdb_analysis_method, cpdb_statistical_analysis_method
from cellphonedb.src.exceptions.ParseCountsException import ParseCountsException


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

    def cpdb_statistical_analysis_launcher(self,
                                           meta: pd.DataFrame,
                                           counts: pd.DataFrame,
                                           iterations: int,
                                           threshold: float,
                                           threads: int,
                                           debug_seed: int,
                                           result_precision: int
                                           ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):

        if threads < 1:
            core_logger.info('Using Default thread number: %s' % self.default_threads)
            threads = self.default_threads

        if threshold < 0 or threshold > 1:
            raise ThresholdValueException(threshold)

        counts = self._counts_validations(counts, meta)

        interactions = self.database_manager.get_repository('interaction').get_all_expanded(
            only_cellphonedb_interactor=True)
        genes = self.database_manager.get_repository('gene').get_all_expanded()
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()

        deconvoluted, mean_pvalue, means, pvalues, significant_means = \
            cpdb_statistical_analysis_method.call(meta,
                                                  counts,
                                                  interactions,
                                                  genes,
                                                  complex_expanded,
                                                  complex_composition,
                                                  iterations,
                                                  threshold,
                                                  threads,
                                                  debug_seed,
                                                  result_precision)

        return pvalues, means, significant_means, mean_pvalue, deconvoluted

    def cpdb_method_analysis_launcher(self,
                                      meta: pd.DataFrame,
                                      counts: pd.DataFrame,
                                      threshold: float,
                                      result_precision: int,
                                      ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):

        if threshold < 0 or threshold > 1:
            raise ThresholdValueException(threshold)

        counts = self._counts_validations(counts, meta)

        interactions = self.database_manager.get_repository('interaction').get_all_expanded(
            only_cellphonedb_interactor=True)
        genes = self.database_manager.get_repository('gene').get_all_expanded()
        complex_composition = self.database_manager.get_repository('complex').get_all_compositions()
        complex_expanded = self.database_manager.get_repository('complex').get_all_expanded()

        means, significant_means, deconvoluted = cpdb_analysis_method.call(
            meta,
            counts,
            interactions,
            genes,
            complex_expanded,
            complex_composition,
            threshold,
            result_precision)

        return means, significant_means, deconvoluted

    def _counts_validations(self, counts: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
        if not len(counts.columns):
            raise ParseCountsException('Counts values are not decimal values', 'Incorrect file format')
        try:
            counts = counts.astype(pd.np.float)  # type: pd.DataFrame
        except:
            raise ParseCountsException
        for cell in meta.index.values:
            if cell not in counts.columns.values:
                raise ParseCountsException('Some cells in meta didnt exist in counts columns',
                                           'Maybe incorrect file format')
        return counts
