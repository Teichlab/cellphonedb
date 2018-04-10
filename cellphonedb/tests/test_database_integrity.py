import pandas as pd
from flask_testing import TestCase

from cellphonedb import extensions
from cellphonedb.flask_app import create_app, output_dir
from cellphonedb.core.models.gene.db_model_gene import Gene


class DatabaseIntegrity(TestCase):
    def test_gene(self):
        query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Gene)
        dataframe = pd.read_sql(query.statement,
                                extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)

        duplicated_genes = dataframe[dataframe.duplicated(keep=False)]
        if len(duplicated_genes):
            duplicated_genes.sort_values('gene_name').to_csv('%s/WARNING_duplicated_genes.csv' % output_dir,
                                                             index=False)

        self.assertEqual(len(duplicated_genes), 0,
                         'There are %s duplicated genes in database. Please check WARNING_duplicated_genes.csv file' % len(
                             duplicated_genes))

    def create_app(self):
        return create_app(raise_non_defined_vars=False)
