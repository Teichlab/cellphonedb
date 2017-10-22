from flask_script import Manager

from tools.app import create_app
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins

app = create_app()
manager = Manager(app)


@manager.command
def merge_duplicated_proteins(filename):
    with app.app_context():
        merge_proteins(filename)


if __name__ == "__main__":
    manager.run()
