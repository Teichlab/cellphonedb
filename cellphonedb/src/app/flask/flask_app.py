from flask import Flask
from flask_restful import Api

from cellphonedb.src.api_endpoints.web_api import routes
from cellphonedb.src.app import app_config
from cellphonedb.src.app.cellphonedb_app import cellphonedb_app


def create_app(environment=None, support=None, load_defaults=None, raise_non_defined_vars=True, verbose=None):
    app = Flask(__name__)
    config = app_config.AppConfig(environment, support, load_defaults, raise_non_defined_vars, verbose=verbose)

    cellphone_config = config.get_cellphone_core_config()

    cellphonedb_app.init_app(cellphone_config)

    flask_config = config.flask_config()
    app.config.from_mapping(flask_config)
    app.url_map.strict_slashes = False

    api = Api(app, prefix=flask_config['API_PREFIX'])

    routes.add(api, '/v1')

    return app
