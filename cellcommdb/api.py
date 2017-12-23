import os

from flask import Flask
from flask_restful import Api

from cellcommdb.api_endpoints import routes
from cellcommdb.app import import_config
from cellcommdb.extensions import db

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = '%s/../out/' % current_dir
data_dir = '%s/data/' % current_dir
temp_dir = '%s/temp/' % current_dir
query_input_dir = '%s/data/queries' % current_dir

config = None


def create_app():
    global config
    app = Flask(__name__)
    config = import_config.AppConfig()
    flask_config = config.flask_config()
    app.config.from_mapping(flask_config)
    app.url_map.strict_slashes = False

    with app.app_context():
        db.init_app(app)

    api = Api(app, prefix=flask_config['API_PREFIX'])

    routes.add(api)

    return app
