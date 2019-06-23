from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.exporters import complex_exporter, interaction_exporter, protein_exporter, gene_exporter, \
    protein_complex_cellphonedb


class ExporterLauncher(object):
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def __getattribute__(self, name):
        method = object.__getattribute__(self, name)
        if hasattr(method, '__call__'):
            core_logger.info('Exporting {}'.format(name))

        return method

    def protein_complex_cellphonedb(self):
        multidatas = self.database_manager.get_repository('multidata').get_all_expanded(include_gene=False)
        interactions = self.database_manager.get_repository('interaction').get_all()
        return protein_complex_cellphonedb.call(multidatas, interactions)


    def complex(self):
        complexes = self.database_manager.get_repository('complex').get_all()
        multidatas = self.database_manager.get_repository('multidata').get_all()
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions()
        proteins = self.database_manager.get_repository('protein').get_all_expanded()

        return complex_exporter.call(complexes, multidatas, complex_compositions, proteins)

    def interaction(self):
        interactions_expanded = self.database_manager.get_repository('interaction').get_all_expanded(include_gene=False)
        return interaction_exporter.call(interactions_expanded)

    def protein(self):
        proteins_expanded = self.database_manager.get_repository('protein').get_all_expanded()
        return protein_exporter.call(proteins_expanded)

    def gene(self):
        genes_expanded = self.database_manager.get_repository('gene').get_all_expanded()
        output_columns = self.database_manager.get_column_table_names('gene_table') + ['name']
        return gene_exporter.call(genes_expanded, output_columns)
