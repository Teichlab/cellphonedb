from click.testing import CliRunner

from cellphonedb.api_endpoints.terminal_api.query_terminal_api_endpoints.query_terminal_commands import \
    get_interaction_gene
from cellphonedb.flask_app import create_app
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestTerminalQueryInteractionCalls(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    def test_call_get_interactions_gene(self):
        runner = CliRunner()
        result = runner.invoke(get_interaction_gene)

        self.assertEqual(0, result.exit_code, 'terminal call get interactions gene error')
        self.assertTrue('ensembl' in result.output)
        self.assertTrue('gene_name' in result.output)

    def test_call_get_interactions_gene_withparam(self):
        runner = CliRunner()
        result = runner.invoke(get_interaction_gene, ['--columns=ensembl'])

        self.assertEqual(0, result.exit_code, 'terminal call get interactions gene error')
        self.assertTrue('ensembl' in result.output)
        self.assertTrue('gene_name' not in result.output)
