import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.database.Repository import Repository
from cellphonedb.src.core.database.sqlalchemy_models.db_model_gene import Gene
from cellphonedb.src.core.database.sqlalchemy_models.db_model_multidata import Multidata
from cellphonedb.src.core.database.sqlalchemy_models.db_model_protein import Protein
from cellphonedb.src.core.utils import filters


class GeneRepository(Repository):
    name = 'gene'

    def get_all(self):
        query = self.database_manager.database.session.query(Gene)
        result = pd.read_sql(query.statement, self.database_manager.database.session.bind)

        return result

    def get_all_expanded(self):
        protein_multidata_join = Protein.protein_multidata_id == Multidata.id_multidata
        gene_protein_join = Gene.protein_id == Protein.id_protein
        query = self.database_manager.database.session.query(Gene, Protein, Multidata).join(
            Protein, gene_protein_join).join(Multidata, protein_multidata_join)

        result = pd.read_sql(query.statement, self.database_manager.database.session.bind)

        return result

    def add(self, genes: pd.DataFrame):
        query_multidatas = self.database_manager.database.session.query(Protein.id_protein, Multidata.name).join(
            Multidata)
        multidatas = pd.read_sql(query_multidatas.statement, self.database_manager.database.session.bind)

        genes = self._blend_multidata(genes, ['name'], multidatas)

        genes.rename(index=str, columns={'id_protein': 'protein_id'}, inplace=True)
        genes = filters.remove_not_defined_columns(genes, self.database_manager.get_column_table_names('gene_table'))

        genes.to_sql(name='gene_table', if_exists='append', con=self.database_manager.database.engine, index=False,
                     chunksize=50)

    @staticmethod
    def _blend_multidata(original_data: pd.DataFrame, original_column_names: list, multidatas: pd.DataFrame,
                         quiet: bool = False) -> pd.DataFrame:
        """
        Merges dataframe with multidata names in multidata ids
        """
        if quiet:
            core_logger.debug('Blending proteins in quiet mode')

        result = GeneRepository.blend_dataframes(original_data, original_column_names, multidatas, 'name', 'multidata')

        return result
