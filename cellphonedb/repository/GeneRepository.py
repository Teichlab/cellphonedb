import pandas as pd

from cellphonedb.database.Repository import Repository
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein
from cellphonedb.tools import filters


class GeneRepository(Repository):
    name = 'gene'

    def get_all(self):
        query = self.database_manager.database.session.query(Gene)
        result = pd.read_sql(query.statement, self.database_manager.database.session.bind)

        return result

    def get_all_expanded(self):
        query = self.database_manager.database.session.query(Gene, Protein, Multidata).join(Protein).join(Multidata)
        result = pd.read_sql(query.statement, self.database_manager.database.session.bind)

        return result

    def add(self, genes: pd.DataFrame):
        query_multidatas = self.database_manager.database.session.query(Protein.id_protein, Multidata.name).join(
            Multidata)
        multidatas = pd.read_sql(query_multidatas.statement, self.database_manager.database.session.bind)

        genes = self._blend_multidata(genes, ['name'], multidatas)
        genes = filters.remove_not_defined_columns(genes, self.database_manager.get_column_table_names('gene'))

        genes.to_sql(name='gene', if_exists='append', con=self.database_manager.database.engine, index=False)

    @staticmethod
    def _blend_multidata(original_data: pd.DataFrame, original_column_names: list, multidatas: pd.DataFrame,
                         quiet: bool = False) -> pd.DataFrame:
        """
        Merges dataframe with multidata names in multidata ids
        """
        if quiet:
            print('Blending proteins in quiet mode')

        result = GeneRepository.blend_dataframes(original_data, original_column_names, multidatas, 'name', 'multidata')

        return result
