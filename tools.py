from flask_script import Manager

import click
from flask import Flask
from tools.app import create_app
from tools.merge_duplicated_proteins import merge_duplicated_proteins as merge_proteins
from tools.merge_gene_mouse import merge_gene_mouse as merge_gene
from tools.proteins_actions import generate_inweb_interactions as protein_generate_inweb, only_noncomplex_interactions

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


@manager.command
def generate_inweb(database_proteins, inweb_inbiomap_file):
    with app.app_context():
        protein_generate_inweb(database_proteins, inweb_inbiomap_file)


@manager.command
def generate_inweb_noncomplex(complexes_namefile, inweb_namefile):
    with app.app_context():
        only_noncomplex_interactions(complexes_namefile, inweb_namefile)


if __name__ == "__main__":
    manager.run()
