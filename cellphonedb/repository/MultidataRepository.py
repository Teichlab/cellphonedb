import pandas as pd

from cellphonedb.database.Repository import Repository
from cellphonedb.models.complex.db_model_complex import Complex
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


class MultidataRepository(Repository):
    name = 'multidata'

    def get_all(self):
        query = self.database_manager.database.session.query(Multidata)
        result = pd.read_sql(query.statement, self.database_manager.database.engine)

        return result

    def get_all_expanded(self):
        query_single = self.database_manager.database.session.query(Gene, Protein, Multidata).join(Protein).join(
            Multidata)
        multidata_simple = pd.read_sql(query_single.statement, self.database_manager.database.engine)

        query_complex = self.database_manager.database.session.query(Multidata, Complex).join(Complex)
        multidata_complex = pd.read_sql(query_complex.statement, self.database_manager.database.engine)

        multidata_expanded = multidata_simple.append(multidata_complex, ignore_index=True)

        return multidata_expanded

    def get_multidatas_from_string(self, input_string: str) -> pd.DataFrame:
        multidatas = self.get_all_expanded()

        return multidatas[(multidatas['name'] == input_string) |
                          (multidatas['ensembl'] == input_string) |
                          (multidatas['entry_name'] == input_string) |
                          (multidatas['gene_name'] == input_string)]
