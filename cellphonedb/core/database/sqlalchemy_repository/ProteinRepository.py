import pandas as pd

from cellphonedb.core.database.Repository import Repository
from cellphonedb.core.database.sqlalchemy_models.db_model_multidata import Multidata
from cellphonedb.core.database.sqlalchemy_models.db_model_protein import Protein


class ProteinRepository(Repository):
    name = 'protein'

    def get_all(self) -> pd.DataFrame:
        protein_query = self.database_manager.database.session.query(Protein)
        protein = pd.read_sql(protein_query.statement, self.database_manager.database.session.bind)

        return protein

    def get_all_expanded(self) -> pd.DataFrame:
        protein_query = self.database_manager.database.session.query(Protein, Multidata).join(Multidata)
        protein = pd.read_sql(protein_query.statement, self.database_manager.database.session.bind)

        return protein

    def get_all_name_id(self) -> pd.DataFrame:
        query_multidatas = self.database_manager.database.session.query(Protein.id_protein, Multidata.name).join(
            Multidata)
        multidatas = pd.read_sql(query_multidatas.statement, self.database_manager.database.session.bind)

        return multidatas

    def get_protein_multidata_by_uniprot(self, uniprot: str) -> pd.DataFrame:
        protein_query = self.database_manager.database.session.query(Protein, Multidata).join(Multidata).filter_by(
            name=uniprot).limit(1)
        protein = pd.read_sql(protein_query.statement, self.database_manager.database.session.bind)

        if not protein.empty:
            return protein.iloc[0, :]
        return None

    def add_proteins(self, proteins: pd.DataFrame, multidatas: pd.DataFrame):
        multidatas.to_sql(name='multidata', if_exists='append', con=self.database_manager.database.engine, index=False,
                          chunksize=50)

        multidata_query = self.database_manager.database.session.query(Multidata.id_multidata, Multidata.name)
        multidatas_db = pd.read_sql(multidata_query.statement, self.database_manager.database.session.bind)
        multidatas_db.rename(index=str, columns={'id_multidata': 'protein_multidata_id'}, inplace=True)
        proteins_to_add = pd.merge(proteins, multidatas_db, on='name')
        proteins_to_add.drop('name', inplace=True, axis=1)

        proteins_to_add.to_sql(name='protein', if_exists='append', con=self.database_manager.database.engine,
                               index=False, chunksize=50)
