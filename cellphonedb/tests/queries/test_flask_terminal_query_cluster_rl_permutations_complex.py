from cellphonedb.flask_app import create_app, data_test_dir, output_test_dir
from cellphonedb.flask_terminal_query_launcher import FlaskTerminalQueryLauncher
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestHumanInteractionsPermutationsComplex(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    # TODO: remove after refactor
    # def test_real_data(self):
    #     iterations = 100
    #     data = 'original_prefiltered'
    #
    #     self.query_call(data, iterations)

    def test_test_data(self):
        iterations = 10
        data = 'test'
        self.query_call(data, iterations)

    def test_manual_data(self):
        iterations = 1000
        data = 'manual'
        self.query_call(data, iterations)

    def query_call(self, data, iterations):
        means_base_name = 'complex_means__data-{}_it-{}'.format(data, iterations)
        pvalues_base_name = 'complex_pvalues__data-{}_it-{}'.format(data, iterations)
        result_means_namefile = self.get_test_namefile(means_base_name, 'txt')
        result_pvalues_namefile = self.get_test_namefile(pvalues_base_name, 'txt')

        meta_namefile = 'hi_{}_meta.txt'.format(data)
        counts_namefile = 'hi_{}_counts.txt'.format(data)

        FlaskTerminalQueryLauncher().cluster_rl_permutations_complex(meta_namefile, counts_namefile, iterations,
                                                                     data_test_dir,
                                                                     output_test_dir, result_means_namefile,
                                                                     result_pvalues_namefile, '0')
