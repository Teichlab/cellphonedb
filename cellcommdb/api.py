import os

from cellcommdb.api_endpoints.queries import CellToCluster, ReceptorLigandsInteractions
from flask import Flask
from flask_restful import Api

from cellcommdb.config import BaseConfig
from cellcommdb.extensions import db

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = '%s/../out/' % current_dir
data_dir = '%s/data/' % current_dir
temp_dir = '%s/temp/' % current_dir
query_input_dir = '%s/data/queries' % current_dir

def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False

    with app.app_context():
        db.init_app(app)

    api = Api(app, prefix=config.API_PREFIX)

    api.add_resource(CellToCluster, '/cell_to_cluster')
    api.add_resource(ReceptorLigandsInteractions, '/receptor_ligands_interactions')

    return app
