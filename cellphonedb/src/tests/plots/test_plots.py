import os
import unittest

from cellphonedb.src.app.cellphonedb_app import output_test_dir, data_test_dir
from cellphonedb.src.plotters.r_plotter import dot_plot


class TestPlots(unittest.TestCase):
    def test_dot_plot_with_all_columns_and_rows(self):
        means_path = self._get_input_file_path_for('means')
        pvalues_path = self._get_input_file_path_for('pvalues')
        plot_output = 'dot_plot_output_all_rows_columns.png'

        dot_plot(means_path=means_path,
                 pvalues_path=pvalues_path,
                 output_path=output_test_dir,
                 output_name=plot_output
                 )

        output_path = os.path.join(output_test_dir, plot_output)
        self.assertTrue(os.path.exists(output_path), 'Plot of type dot_plot did not work')
        self.assertGreater(os.path.getsize(output_path), 0)

    def test_dot_plot_with_custom_columns_and_rows(self):
        means_path = self._get_input_file_path_for('means')
        pvalues_path = self._get_input_file_path_for('pvalues')
        columns_file = self._get_fixture('dot_plot_columns.txt')
        rows_file = self._get_fixture('dot_plot_rows.txt')
        plot_output = 'dot_plot_output_custom_rows_columns.png'

        dot_plot(means_path=means_path,
                 pvalues_path=pvalues_path,
                 output_path=output_test_dir,
                 output_name=plot_output,
                 rows=rows_file,
                 columns=columns_file
                 )

        output_path = os.path.join(output_test_dir, plot_output)
        self.assertTrue(os.path.exists(output_path), 'Plot of type dot_plot did not work')
        self.assertGreater(os.path.getsize(output_path), 0)

    @staticmethod
    def _get_input_file_path_for(kind):
        template = 'input_for_plot_statistical_analysis__{}_result__data-test_it-10_seed-0_threshold-01_precision-1.txt'

        return os.path.join(data_test_dir, template.format(kind))

    @staticmethod
    def _get_fixture(name):
        return os.path.join(data_test_dir, name)

