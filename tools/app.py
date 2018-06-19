import os

from flask import Flask, abort

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = '%s/data' % current_dir
output_dir = '%s/out' % current_dir
downloads_dir = '{}/downloads'.format(data_dir)


def create_app():
    app = Flask(__name__)

    return app
