from flask_script import Manager

from tools.app import create_app
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.merge_gene_mouse import merge_gene_mouse as merge_gene

app = create_app()
manager = Manager(app)


@manager.command
def merge_duplicated_proteins(filename):
    with app.app_context():
        merge_proteins(filename)


@manager.command
def merge_gene_mouse(filename_gene, filename_gene_mouse):
    with app.app_context():
        merge_gene(filename_gene, filename_gene_mouse)


if __name__ == "__main__":
    manager.run()
