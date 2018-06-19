from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestFlaskTerminalQueryClusterStatisticalAnalysisComplex(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    # TODO: remove after refactor
    # def test_real_data(self):
    #     iterations = 100
    #     data = 'original_prefiltered'
    #
    #     self.query_call(data, iterations)

    def test_test_data(self):
        iterations = 2
        data = 'test'
        self.query_call(data, iterations, '0')

    def test_manual_data(self):
        iterations = 2
        data = 'manual'
        self.query_call(data, iterations, '0')

    def query_call(self, data, iterations, debug_seed: str):
        means_base_name = 'complex_means__data-{}_it-{}'.format(data, iterations)
        pvalues_base_name = 'complex_pvalues__data-{}_it-{}'.format(data, iterations)
        significant_means_base_name = 'complex_significant_mean__data-{}_it-{}'.format(data, iterations)
        pvalues_means_base_name = 'complex_pvalues_means__data-{}_it-{}'.format(data, iterations)
        deconvoluted_base_name = 'complex_deconvoluted__data-{}_it-{}'.format(data, iterations)

        result_means_filename = self.get_test_filename(means_base_name, 'txt')
        result_pvalues_filename = self.get_test_filename(pvalues_base_name, 'txt')
        result_significant_means_filename = self.get_test_filename(significant_means_base_name, 'txt')
        result_pvalues_means_filename = self.get_test_filename(pvalues_means_base_name, 'txt')
        deconvoluted_filename = self.get_test_filename(deconvoluted_base_name, 'txt')

        meta_filename = 'hi_{}_meta.txt'.format(data)
        counts_filename = 'hi_{}_counts.txt'.format(data)

        FlaskTerminalQueryLauncher().cluster_statistical_analysis_complex(meta_filename, counts_filename, iterations,
                                                                          data_test_dir,
                                                                          output_test_dir, result_means_filename,
                                                                          result_pvalues_filename,
                                                                          result_significant_means_filename,
                                                                          result_pvalues_means_filename,
                                                                          deconvoluted_filename,
                                                                          debug_seed)
