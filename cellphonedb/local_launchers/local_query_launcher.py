from cellphonedb.app.app_logger import app_logger


class LocalQueryLauncher:
    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            app_logger.info('Launching Query {}'.format(name))

        return method

    def __init__(self, cellphonedb_app):

        self.cellphonedb_app = cellphonedb_app

    def find_interactions_by_element(self, element: str) -> None:
        print(self.cellphonedb_app.cellphonedb.query.find_interactions_by_element(element).to_csv(index=False))

    def get_interaction_gene(self, columns: str) -> None:
        if columns:
            columns = columns.split(',')

        print(self.cellphonedb_app.cellphonedb.query.get_interaction_gene(columns).to_csv(index=False))

    def cpdb_data_report(self, ) -> None:
        report = self.cellphonedb_app.cellphonedb.query.cpdb_data_report_launcher()

        print('PROTEINS')
        print('========')
        print('* TOTAL PROTEINS %s' % report['total_proteins'])

        print('')
        print('SECRETED PROTEINS')
        print('-----------------')
        print('* ALL SECRETED PROTEINS: %s' % report['secreted_proteins'])
        print('* SECRETED PROTEINS in CPDB INTERACTIONS: %s' % report['secreted_proteins_in_cpdb_interaction'])
        print('* SECRETED PROTEINS with TAG=To_add: %s' % report['secreted_proteins_with_tag_to_add'])
        print('* SECRETED PROTEINS with TAG=`To_add` and in CPDB INTERACTION: %s' % report[
            'secreted_proteins_with_tag_to_add_and_cpdb_interaction'])

        print('')
        print('TRANSMEMBRANE PROTEINS')
        print('----------------------')

        print('* ALL TRANSMEMBRANE PROTEINS: %s' % report['transmembrane_proteins'])
        print('* TRANSMEMBRANE PROTEINS in CPDB INTERACTIONS: %s' % report['transmembrane_proteins_in_cpdb'])
        print('* TRANSMEMBRANE PROTEINS with TAG=To_add: %s' % report['transmembrane_proteins_with_tag_to_add'])
        print('* TRANSMEMBRANE PROTEINS with TAG=`To_add` and in CPDB INTERACTION: %s' % report[
            'transmembrane_proteins_with_tag_to_add_and_cpdb_interaction'])

        print('')
        print('PROTEIN COMPLEX')
        print('-------')
        print('* PROTEINS in COMPLEX: %s ' % report['proteins_in_complex'])
        print('* PROTEINS in CPDB COMPLEX: %s' % report['proteins_in_cpdb_complex'])

        print('')
        print('INTERACTIONS')
        print('------------')
        print('* ALL INTERACTIONS: %s' % report['interactions'])
        print('* INTERACTIONS CPDB INTERACTOR: %s' % report['interactions_cpdb'])
        print('* INTERACTIONS CURATED: %s' % report['interactions_curated'])
        print('* INTERACTIONS CURATED in CPDB INTERACTIONS: %s' % report['interactions_curated_in_cpdb_interactions'])
        print('* INTERACTIONS CURATED EXCLUDED in CPDB by SAME _1/_2 PROTEIN: %s' % report[
            'interaction_protein_duplicated'])

        print('* INTERACTIONS IUPHAR: %s' % report['interactions_iuphar'])
        print('* INTERACTIONS IUPHAR in CPDB INTERACTIONS: %s' % report['interactions_cpdb_iuphar'])

        print('* INTERACTIONS NON CURATED OR IUPHAR: %s' % report['interactions_non_curated_iuphar'])

        print('* INTERACTIONS CPDB NON CURATED OR IUPHAR: %s' % report['interactions_cpdb_non_curated_iuphar'])
