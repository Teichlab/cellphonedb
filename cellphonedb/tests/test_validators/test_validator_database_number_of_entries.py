from cellphonedb.app.cellphonedb_app import cellphonedb_app
from cellphonedb.app.flask.flask_app import create_app
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestValidatorDatabaseNumberOfEntries(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    def test_protein(self):
        proteins = cellphonedb_app.cellphonedb.database_manager.get_repository('protein').get_all()

        self.assertEqual(5278, len(proteins), 'Number of Protein entries are different')

    def test_gene(self):
        genes = cellphonedb_app.cellphonedb.database_manager.get_repository('gene').get_all()
        self.assertEqual(6193, len(genes), 'Number of Gene entries are different')

    def test_complex(self):
        complex = cellphonedb_app.cellphonedb.database_manager.get_repository('complex').get_all()
        self.assertEqual(260, len(complex), 'Number of Complex entries are different')

    def test_multidata(self):
        multidatas = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'multidata').get_all()
        self.assertEqual(5538, len(multidatas), 'Number of Multidata entries are different')

    def test_protein_complex(self):
        multidatas = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'multidata').get_all()
        number_of_multidata = len(multidatas)

        proteins = cellphonedb_app.cellphonedb.database_manager.get_repository('protein').get_all()
        number_of_protein = len(proteins)

        complexes = cellphonedb_app.cellphonedb.database_manager.get_repository('complex').get_all()
        number_of_complex = len(complexes)

        self.assertEqual(number_of_complex + number_of_protein, number_of_multidata,
                         'Number of multidata is diferent than proteins+complex')

    def test_interaction(self):
        interactions = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'interaction').get_all()

        self.assertEqual(10819, len(interactions), 'Number of interactions are not equal')

    def test_interaction_curated(self):
        interactions = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'interaction').get_all()
        self.assertEqual(872, len(interactions[interactions['source'] == 'curated']),
                         'Number of curated interactions not equal')

    def test_interaction_cpdb_interactor(self):
        interactions = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'interaction').get_all()

        self.assertEqual(1144, len(interactions[interactions['is_cellphonedb_interactor']]),
                         'number of cellphonedb interaction interactors different that expected')

    def test_interaction_iuphar(self):
        interactions = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'interaction').get_all()
        self.assertEqual(245, len(interactions[interactions['iuphar']]))

    def test_complex_composition(self):
        complex_compositions = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'complex').get_all_compositions()
        self.assertEqual(546, len(complex_compositions), 'Number of Complex Composition entries are different')

    def setUp(self):
        return create_app(raise_non_defined_vars=False)
