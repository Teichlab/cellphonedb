from cellphonedb.core.exporters import ligands_receptors_proteins_exporter, complex_exporter, complex_web_exporter, \
    interaction_exporter, receptor_ligand_interaction_exporter, protein_exporter, gene_exporter


class ExporterLauncher(object):
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def ligands_receptors_proteins(self):
        genes_expanded = self.database_manager.get_repository('gene').get_all_expanded()
        return ligands_receptors_proteins_exporter.call(genes_expanded)

    def complex(self):
        complexes = self.database_manager.get_repository('complex').get_all()
        multidatas = self.database_manager.get_repository('multidata').get_all()
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions()
        proteins = self.database_manager.get_repository('protein').get_all_expanded()

        return complex_exporter.call(complexes, multidatas, complex_compositions, proteins)

    def complex_web(self):
        complexes = self.database_manager.get_repository('complex').get_all()
        multidatas = self.database_manager.get_repository('multidata').get_all()
        complex_compositions = self.database_manager.get_repository('complex').get_all_compositions()
        proteins = self.database_manager.get_repository('protein').get_all_expanded()

        return complex_web_exporter.call(complexes, multidatas, complex_compositions, proteins)

    def interaction(self):
        interactions_expanded = self.database_manager.get_repository('interaction').get_all_expanded()
        return interaction_exporter.call(interactions_expanded)

    def receptor_ligand_interaction(self):
        interactions_expanded = self.database_manager.get_repository('interaction').get_all_expanded()
        return receptor_ligand_interaction_exporter.call(interactions_expanded)

    def protein(self):
        proteins_expanded = self.database_manager.get_repository('protein').get_all_expanded()
        return protein_exporter.call(proteins_expanded)

    def gene(self):
        genes_expanded = self.database_manager.get_repository('gene').get_all_expanded()
        output_columns = self.database_manager.get_column_table_names('gene') + ['name']
        return gene_exporter.call(genes_expanded, output_columns)
