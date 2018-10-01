from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestWebApiQueryInteractionCalls(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)

    def test_web_api_query_interaction_call(self):
        response = self.client.get(
            '/api/v1/query/interaction/gene')

        self.assert200(response, 'Web api get interactions gene call error')
        self.assertTrue('ensembl' in str(response.data), 'ensembl column should be present in response')
        self.assertTrue('gene_name' in str(response.data), 'gene_name column shoud be present in response')
        self.assertTrue('hgnc_symbol' in str(response.data), 'hgnc_symbol should be present in response')

    def test_web_api_query_interaction_call_parameters(self):
        response = self.client.get(
            '/api/v1/query/interaction/gene?columns=ensembl,gene_name')

        self.assert200(response, 'Web api get interactions gene call with parameters error')
        self.assertTrue('ensembl' in str(response.data), 'ensembl column should be present in response')
        self.assertTrue('gene_name' in str(response.data), 'gene_name column shoud be present in response')
        self.assertTrue('hgnc_symbol' not in str(response.data), 'hgnc_symbol shouldnt be present in response')
