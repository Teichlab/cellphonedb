from cellphonedb.core.collectors import protein_preprocess_collector, gene_preprocess_collector
from cellphonedb.database import DatabaseManager


class Collector(object):
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    def protein(self, proteins):
        multidata_columns = self.database_manager.get_column_table_names('multidata')
        protein_columns = self.database_manager.get_column_table_names('protein')

        proteins_to_add, multidata_to_add = protein_preprocess_collector.call(proteins, multidata_columns,
                                                                              protein_columns)

        self.database_manager.get_repository('protein').add_proteins(proteins_to_add, multidata_to_add)

    def gene(self, genes):
        genes_processed = gene_preprocess_collector.call(genes, self.database_manager.get_column_table_names('gene'))
        self.database_manager.get_repository('gene').add(genes_processed)

    def complex(self, complexes):
        self.database_manager.get_repository('complex').add(complexes)

    # def interaction(self, interaction_file=None):
    #     interaction_collection.load(interaction_file)
    #
    # def all(self, filename=None):
    #     print('Collecting Proteins')
    #     protein_collection.load()
    #     print('Collecting Genes')
    #     gene_collection.load()
    #     print('Collecting Complexes')
    #     complex_collection.load()
    #     print('Collecting Interactions')
    #     interaction_collection.load()
