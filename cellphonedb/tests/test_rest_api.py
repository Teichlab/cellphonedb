import json

from cellphonedb.flask_app import create_app, data_test_dir
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestRestApi(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(environment='test', raise_non_defined_vars=False)

    def setUp(self):
        self.reset_db()
        self.populate_db()


