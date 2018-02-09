from flask_testing import TestCase

from cellphonedb.api import create_app


class TestDatabase(TestCase):
    def create_app(self):
        return create_app(environment='test')

    def test_database_init(self):
        pass
