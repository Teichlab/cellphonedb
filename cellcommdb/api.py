import os

from cellcommdb.api_endpoints.queries import Query0Endpoint, Query1Endpoint
from flask import Flask, abort, request
from flask_restful import Api, Resource

from cellcommdb.config import BaseConfig
from cellcommdb.extensions import db

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = '%s/../out/' % current_dir


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False

    with app.app_context():
        db.init_app(app)

    api = Api(app, prefix=config.API_PREFIX)
    # api.add_resource(ProteinResource, '/protein')
    # api.add_resource(ComplexResource, '/complex')

    api.add_resource(Query0Endpoint, '/query0')
    api.add_resource(Query1Endpoint, '/query1')

    return app
