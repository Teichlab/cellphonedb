import os

from cellcommdb.resources.base import ProteinResource, ComplexResource
from flask import Flask, abort
from flask_restful import Api

from cellcommdb.config import BaseConfig
from cellcommdb.extensions import db


current_dir = os.path.dirname(os.path.realpath(__file__))


def create_app(config=BaseConfig):

    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False

    with app.app_context():
        db.init_app(app)

    api = Api(app, prefix=config.API_PREFIX)
    api.add_resource(ProteinResource, '/protein')
    api.add_resource(ComplexResource, '/complex')

    return app
