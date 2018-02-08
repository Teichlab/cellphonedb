import pandas as pd

from cellphonedb.database.Repository import Repository
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


class GeneRepository(Repository):
    name = 'gene_repository'

    def get_all(self):
        query = self.database.session.query(Gene)
        result = pd.read_sql(query.statement, self.database.session.bind)

        return result

    def get_all_expanded(self):
        query = self.database.session.query(Gene, Protein, Multidata).join(Protein).join(Multidata)
        result = pd.read_sql(query.statement, self.database.session.bind)

        return result
