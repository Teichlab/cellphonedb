import os

from flask import Flask
from flask_restful import Api

from cellphonedb.api_endpoints import routes
from cellphonedb.app import import_config
from cellphonedb.extensions import cellphonedb_flask

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = '%s/../out' % current_dir
data_dir = '%s/data' % current_dir
temp_dir = '%s/temp' % current_dir
query_input_dir = '%s/data/queries' % current_dir

output_test_dir = '{}/tests/out'.format(current_dir)

config = None


def create_app(environment=None, support=None, load_defaults=None):
    global config
    app = Flask(__name__)
    config = import_config.AppConfig(environment, support, load_defaults)
    flask_config = config.flask_config()
    app.config.from_mapping(flask_config)
    app.url_map.strict_slashes = False

    with app.app_context():
        cellphonedb_flask.init_app(app)

    api = Api(app, prefix=flask_config['API_PREFIX'])

    routes.add(api)

    return app
