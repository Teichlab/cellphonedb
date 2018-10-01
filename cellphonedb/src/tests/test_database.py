from flask_testing import TestCase

from cellphonedb.src.app.flask.flask_app import create_app


class TestDatabase(TestCase):
    def create_app(self):
        return create_app(environment='test', raise_non_defined_vars=False)

    def test_database_init(self):
        pass
