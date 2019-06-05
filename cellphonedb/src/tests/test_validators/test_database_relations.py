import pandas as pd
from flask_testing import TestCase

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.core.database.sqlalchemy_models.db_model_gene import Gene
from cellphonedb.src.core.database.sqlalchemy_models.db_model_multidata import Multidata
from cellphonedb.src.core.database.sqlalchemy_models.db_model_protein import Protein


class TestDatabaseRelationsChecks(TestCase):
    def test_all_protein_have_gen(self):

        expected_protein_without_gene = 0
        protein_query = cellphonedb_app.cellphonedb.database_manager.database.session.query(Protein,
                                                                                            Multidata.name).join(
            Multidata)

        protein_df = pd.read_sql(protein_query.statement,
                                 cellphonedb_app.cellphonedb.database_manager.database.engine)
        protein_ids = protein_df['id_protein'].tolist()

        gene_query = cellphonedb_app.cellphonedb.database_manager.database.session.query(
            Gene.protein_id)
        gene_protein_ids = \
            pd.read_sql(gene_query.statement,
                        cellphonedb_app.cellphonedb.database_manager.database.engine)[
                'protein_id'].tolist()

        protein_without_gene = []
        for protein_id in protein_ids:
            if not protein_id in gene_protein_ids:
                protein_without_gene.append(protein_df[protein_df['id_protein'] == protein_id]['name'].iloc[0])

        if len(protein_without_gene) != expected_protein_without_gene:
            app_logger.warning('There are {} Proteins without gene'.format(len(protein_without_gene)))
            app_logger.warning(protein_without_gene)

            unknowed_proteins_without_gene = []
            for protein in protein_without_gene:
                if not protein in KNOWED_PROTEINS_WITHOUT_GENE:
                    unknowed_proteins_without_gene.append(protein)

            if unknowed_proteins_without_gene:
                app_logger.warning(
                    'There are {} unknowed proteins without gene'.format(len(unknowed_proteins_without_gene)))
                app_logger.warning(pd.Series(unknowed_proteins_without_gene).drop_duplicates().tolist())

        self.assertEqual(expected_protein_without_gene, len(protein_without_gene), 'There are Proteins without Gene.')

    def test_gene_are_not_duplicated(self):
        query = cellphonedb_app.cellphonedb.database_manager.database.session.query(Gene)
        dataframe = pd.read_sql(query.statement,
                                cellphonedb_app.cellphonedb.database_manager.database.engine)

        duplicated_genes = dataframe[dataframe.duplicated(keep=False)]
        if len(duplicated_genes):
            app_logger.warning(duplicated_genes.sort_values('gene_name').to_csv(index=False))

        self.assertEqual(
            len(duplicated_genes), 0,
            'There are %s not not expected duplicated genes in database. '
            'Please check WARNING_duplicated_genes.csv file' % len(duplicated_genes))

    def test_duplicated_gene_ensembl_is_not_in_interaction(self):
        all_genes = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'gene').get_all_expanded()
        all_interactions = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'interaction').get_all()

        genes_duplicated_ensembl = all_genes[all_genes.duplicated('ensembl', keep=False)]

        all_interactions_multidata_ids = all_interactions['multidata_1_id'].tolist() + all_interactions[
            'multidata_2_id'].tolist()

        duplicated_gene_ensembls_in_interactions = genes_duplicated_ensembl[
            genes_duplicated_ensembl['id_multidata'].apply(lambda id: id in all_interactions_multidata_ids)]

        nunknowed_duplicated_ensembl = False
        if not duplicated_gene_ensembls_in_interactions[
            duplicated_gene_ensembls_in_interactions['ensembl'].apply(
                lambda ensembl: ensembl not in KNOWED_DUPLICATED_ENSEMBL.tolist())].empty:
            app_logger.warning('Some duplicated ensembls apears in interactions')
            app_logger.warning(duplicated_gene_ensembls_in_interactions.to_csv(index=False))
            nunknowed_duplicated_ensembl = True

        self.assertFalse(nunknowed_duplicated_ensembl,
                         'Some duplicated ensembl gene apears in interactions')
        self.assertFalse(
            len(KNOWED_DUPLICATED_ENSEMBL.drop_duplicates()) !=
            len(duplicated_gene_ensembls_in_interactions.drop_duplicates('ensembl')),
            'Some duplicated ensembl gene apears in interactions')

    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)


KNOWED_DUPLICATED_ENSEMBL = pd.Series(['ENSG00000110680'])
KNOWED_PROTEINS_WITHOUT_GENE = []
