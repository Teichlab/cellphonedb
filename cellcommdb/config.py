import os


class BaseConfig(object):

   SECRET_KEY = '5e7ca92615435457f491e6546ee4b092a6497a47d894bb21'
   SQLALCHEMY_DATABASE_URI = os.environ.get('CELLCOMMDB_URI')
   API_PREFIX = '/api'
   DEBUG = True


class TestConfig(BaseConfig):

   SQLALCHEMY_DATABASE_URI = os.environ.get('CELLCOMMDB_TEST_URI')
