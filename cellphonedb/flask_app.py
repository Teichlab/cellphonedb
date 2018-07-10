import os

from flask import Flask
from flask_restful import Api

from cellphonedb.api_endpoints.web_api import routes
from cellphonedb.app import import_config
from cellphonedb.extensions import cellphonedb_flask

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = '%s/../out' % current_dir
data_dir = '%s/core/data' % current_dir
temp_dir = '%s/temp' % current_dir
query_input_dir = '%s/../in' % current_dir

output_test_dir = '{}/tests/out'.format(current_dir)
data_test_dir = '{}/tests/fixtures'.format(current_dir)


def create_app(environment=None, support=None, load_defaults=None, raise_non_defined_vars=True):
    app = Flask(__name__)
    config = import_config.AppConfig(environment, support, load_defaults, raise_non_defined_vars)

    cellphone_config = config.get_cellphone_core_config()

    cellphonedb_flask.init_app(cellphone_config)

    flask_config = config.flask_config()
    app.config.from_mapping(flask_config)
    app.url_map.strict_slashes = False

    api = Api(app, prefix=flask_config['API_PREFIX'])

    routes.add(api, '/v1')

    return app
