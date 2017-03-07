from flask.ext.script import Manager

from cellcommdb.api import create_app
from cellcommdb.extensions import db
from cellcommdb.db_scripts import db_drop_everything
from cellcommdb.models import *


app = create_app()
manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def create_db():
    with app.app_context():
        db.create_all()


@manager.command
def reset_db():
    with app.app_context():
        db_drop_everything(db)
        db.create_all()


if __name__ == "__main__":
    manager.run()
