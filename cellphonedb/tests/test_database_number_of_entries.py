from cellphonedb import extensions
from cellphonedb.flask_app import create_app
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestDatabaseNumberOfEntries(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app()

    def test_protein(self):
        proteins = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('protein').get_all()

        self.assertEqual(len(proteins), 5269, 'Number of Protein entries are different')

    def test_gene(self):
        genes = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('gene').get_all()
        self.assertEqual(len(genes), 6394, 'Number of Gene entries are different')

    def test_complex(self):
        complex = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('complex').get_all()
        self.assertEqual(len(complex), 247, 'Number of Complex entries are different')

    def test_multidata(self):
        multidatas = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('multidata').get_all()
        self.assertEqual(len(multidatas), 5516, 'Number of Multidata entries are different')

    def test_protein_complex(self):
        multidatas = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('multidata').get_all()
        number_of_multidata = len(multidatas)

        proteins = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('protein').get_all()
        number_of_protein = len(proteins)

        complexes = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('complex').get_all()
        number_of_complex = len(complexes)

        self.assertEqual(number_of_multidata, number_of_complex + number_of_protein,
                         'Number of multidata is diferent than proteins+complex')

    def test_interaction(self):
        interactions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('interaction').get_all()

        self.assertEqual(len(interactions), 10500, 'Number of interactions not equal')

    def test_interaction_curated(self):
        interactions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('interaction').get_all()
        self.assertEqual(len(interactions[interactions['source'] == 'curated']), 477,
                         'Number of curated interactions not equal')

    def test_complex_composition(self):
        complex_compositions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository(
            'complex').get_all_compositions()
        self.assertEqual(len(complex_compositions), 519, 'Number of Complex Composition entries are different')

    def setUp(self):
        return create_app()
