import os

from flask import Flask, abort

current_dir = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask(__name__)

    return app
