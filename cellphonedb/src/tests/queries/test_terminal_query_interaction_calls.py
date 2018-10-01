from click.testing import CliRunner

from cellphonedb.src.api_endpoints.terminal_api.query_terminal_api_endpoints.query_terminal_commands import \
    get_interaction_gene
from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestTerminalQueryInteractionCalls(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)

    def test_call_get_interactions_gene(self):
        runner = CliRunner()
        result = runner.invoke(get_interaction_gene)

        self.assertEqual(0, result.exit_code, 'terminal call get interactions gene error')
        self.assertTrue('ensembl' in str(result.output), 'ensembl column should be present in response')
        self.assertTrue('gene_name' in str(result.output), 'gene_name column shoud be present in response')
        self.assertTrue('hgnc_symbol' in str(result.output), 'hgnc_symbol should be present in response')

    def test_call_get_interactions_gene_withparam(self):
        runner = CliRunner()
        result = runner.invoke(get_interaction_gene, ['--columns=ensembl,gene_name'])

        self.assertEqual(0, result.exit_code, 'terminal call get interactions gene error')
        self.assertTrue('ensembl' in str(result.output), 'ensembl column should be present in response')
        self.assertTrue('gene_name' in str(result.output), 'gene_name column shoud be present in response')
        self.assertTrue('hgnc_symbol' not in str(result.output), 'hgnc_symbol shouldnt be present in response')
