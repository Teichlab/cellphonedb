import pandas as pd

from cellphonedb.database.Repository import Repository
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


class ProteinRepository(Repository):
    name = 'protein'

    def get_all(self):
        protein_query = self.database_manager.database.session.query(Protein)
        protein = pd.read_sql(protein_query.statement, self.database_manager.database.session.bind)

        return protein

    def get_all_expanded(self):
        protein_query = self.database_manager.database.session.query(Protein, Multidata).join(Multidata)
        protein = pd.read_sql(protein_query.statement, self.database_manager.database.session.bind)

        return protein

    def get_protein_multidata_by_uniprot(self, uniprot):
        """

        :type uniprot: str
        :rtype: pd.Series
        """
        protein_query = self.database_manager.database.session.query(Protein, Multidata).join(Multidata).filter_by(
            name=uniprot).limit(1)
        protein = pd.read_sql(protein_query.statement, self.database_manager.database.session.bind)

        if not protein.empty:
            return protein.iloc[0, :]
        return None
