import json
from flask.ext.testing import TestCase

from cellcommdb.config import TestConfig
from cellcommdb.api import create_app
from cellcommdb.collection import collect_proteins
from cellcommdb.extensions import db


class TestResource(TestCase):

    def test_protein(self):
        test_data = self.fetch_data('/api/protein')[0]
        assert test_data['uniprot'] is not None

    def fetch_data(self, *args, **kwargs):

        result = self.client.get(*args, **kwargs)
        return json.loads(result.data.decode('utf-8'))

    def create_app(self):

        return create_app(TestConfig)

    def _populate_db(self):

        with self.app.app_context():
            collect_proteins(self.app)

    def setUp(self):
        self._clear_db()
        db.create_all()
        self._populate_db()

        self.client = self.app.test_client()

    @staticmethod
    def _clear_db():
        db.session.remove()
        db.reflect()
        db.drop_all()