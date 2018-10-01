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

        expected_protein_without_gene = 235
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

        self.assertEqual(len(duplicated_genes), 0,
                         'There are %s duplicated genes in database. Please check WARNING_duplicated_genes.csv file' % len(
                             duplicated_genes))

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

        if not duplicated_gene_ensembls_in_interactions.empty:
            app_logger.warning('Some duplicated ensembls apears in interactions')
            app_logger.warning(duplicated_gene_ensembls_in_interactions.to_csv(index=False))

        self.assertTrue(duplicated_gene_ensembls_in_interactions.empty,
                        'Some duplicated ensembl gene apears in interactions')

    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)


KNOWED_PROTEINS_WITHOUT_GENE = ['P01889', 'P01891', 'P01892', 'P03989', 'P04222', 'P04439', 'P05534', 'P06340',
                                'P10314', 'P10316', 'P10319', 'P10321', 'P13746', 'P13765', 'P16188', 'P16189',
                                'P16190', 'P18462', 'P18463', 'P18464', 'P18465', 'P28067', 'P28068', 'P30443',
                                'P30447', 'P30450', 'P30453', 'P30455', 'P30456', 'P30457', 'P30459', 'P30460',
                                'P30461', 'P30462', 'P30464', 'P30466', 'P30475', 'P30479', 'P30480', 'P30481',
                                'P30483', 'P30484', 'P30485', 'P30486', 'P30487', 'P30488', 'P30490', 'P30491',
                                'P30492', 'P30493', 'P30495', 'P30498', 'P30499', 'P30501', 'P30504', 'P30505',
                                'P30508', 'P30510', 'P30511', 'P30512', 'P30685', 'Q04826', 'Q07000', 'Q09160',
                                'Q29718', 'Q29836', 'Q29865', 'Q29940', 'Q29963', 'Q31610', 'Q31612', 'Q95365',
                                'Q95604', 'Q9TNN7', 'Q5TFQ8', 'Q5VU13', 'P06881', 'O95467', 'P01903', 'P01906',
                                'P01909', 'P01911', 'P01912', 'P01920', 'P04229', 'P04440', 'P05538', 'P13760',
                                'P13761', 'P13762', 'P20036', 'P20039', 'P58400', 'P79483', 'Q29960', 'Q29974',
                                'Q30134', 'Q30154', 'Q30167', 'Q30201', 'Q30KQ2', 'Q5Y7A7', 'Q6UXV3', 'Q8WXG9',
                                'Q95IE3', 'Q9BZG9', 'Q9GIY3', 'Q9NPA2', 'Q9TQE0', 'Q9UHI7', 'P01782', 'A8MVG2',
                                'Q8NGJ3', 'P0C617', 'P0C7N5', 'O42043', 'O71037', 'P61565', 'P61566', 'Q69384',
                                'Q902F8', 'Q9UKH3', 'P84996', 'Q902F9', 'P63092', 'A6NIZ1', 'P60507', 'P87889',
                                'Q9YNA8', 'P62683', 'P63145', 'P61570', 'Q9HDB9', 'Q7LDI9', 'P61567', 'P63130',
                                'P62685', 'P63126', 'P63128', 'P60509', 'P61550', 'P62684', 'Q9N2J8', 'Q9N2K0',
                                'P04435', 'A6NKC4', 'A6NJS3', 'A6NJ16', 'Q96I85', 'Q5TEV5', 'Q96LR1', 'Q71RG6',
                                'Q6IE37', 'Q6IE36', 'Q9P1C3', 'A8MTI9', 'Q6UY13', 'A8MTW9', 'A8MUN3', 'Q6ZRU5',
                                'Q6UXQ8', 'Q6UXR6', 'Q6UXU0', 'Q13072', 'Q86Y29', 'Q86Y28', 'Q86Y27']
