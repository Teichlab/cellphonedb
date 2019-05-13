import os

from flask import Flask

this_file_dir = os.path.dirname(os.path.realpath(__file__))


data_dir = '{}/data'.format(this_file_dir)
output_dir = '{}/out'.format(this_file_dir)
downloads_dir = '{}/downloads'.format(data_dir)


def create_app():
    app = Flask(__name__)

    return app
