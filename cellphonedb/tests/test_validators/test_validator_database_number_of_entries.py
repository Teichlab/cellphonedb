from cellphonedb import extensions
from cellphonedb.flask_app import create_app
from cellphonedb.tests.cellphone_flask_test_case import CellphoneFlaskTestCase


class TestValidatorDatabaseNumberOfEntries(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False)

    def test_protein(self):
        proteins = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('protein').get_all()

        self.assertEqual(5272, len(proteins), 'Number of Protein entries are different')

    def test_gene(self):
        genes = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('gene').get_all()
        self.assertEqual(6186, len(genes), 'Number of Gene entries are different')

    def test_complex(self):
        complex = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('complex').get_all()
        self.assertEqual(260, len(complex), 'Number of Complex entries are different')

    def test_multidata(self):
        multidatas = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('multidata').get_all()
        self.assertEqual(5532, len(multidatas), 'Number of Multidata entries are different')

    def test_protein_complex(self):
        multidatas = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('multidata').get_all()
        number_of_multidata = len(multidatas)

        proteins = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('protein').get_all()
        number_of_protein = len(proteins)

        complexes = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('complex').get_all()
        number_of_complex = len(complexes)

        self.assertEqual(number_of_complex + number_of_protein, number_of_multidata,
                         'Number of multidata is diferent than proteins+complex')

    def test_interaction(self):
        interactions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('interaction').get_all()

        self.assertEqual(10735, len(interactions), 'Number of interactions are not equal')

    def test_interaction_curated(self):
        interactions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('interaction').get_all()
        self.assertEqual(795, len(interactions[interactions['source'] == 'curated']),
                         'Number of curated interactions not equal')

    def test_interaction_iuphar(self):
        interactions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository('interaction').get_all()
        self.assertEqual(241, len(interactions[interactions['iuphar']]))

    def test_complex_composition(self):
        complex_compositions = extensions.cellphonedb_flask.cellphonedb.database_manager.get_repository(
            'complex').get_all_compositions()
        self.assertEqual(546, len(complex_compositions), 'Number of Complex Composition entries are different')

    def setUp(self):
        return create_app(raise_non_defined_vars=False)
