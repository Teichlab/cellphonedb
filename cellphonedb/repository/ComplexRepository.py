import pandas as pd

from cellphonedb.database.Repository import Repository
from cellphonedb.models.complex.db_model_complex import Complex
from cellphonedb.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellphonedb.models.multidata.db_model_multidata import Multidata


class ComplexRepository(Repository):
    name = 'complex'

    def get_all(self) -> pd.DataFrame:
        query = self.database_manager.database.session.query(Complex)
        result = pd.read_sql(query.statement, self.database_manager.database.engine)

        return result

    def get_all_expanded(self) -> pd.DataFrame:
        query = self.database_manager.database.session.query(Complex, Multidata).join(Multidata)
        result = pd.read_sql(query.statement, self.database_manager.database.engine)

        return result

    def get_all_compositions(self) -> pd.DataFrame:
        query = self.database_manager.database.session.query(ComplexComposition)
        result = pd.read_sql(query.statement, self.database_manager.database.engine)

        return result

    def get_all_compositions_expanded(self, suffixes=None) -> pd.DataFrame:
        if not suffixes:
            suffixes = ['_complex', '_protein']

        query = self.database_manager.database.session.query(ComplexComposition)
        complex_composition = pd.read_sql(query.statement, self.database_manager.database.engine)

        multidata_query = self.database_manager.database.session.query(Multidata)
        multidatas = pd.read_sql(multidata_query.statement, self.database_manager.database.engine)

        complex_composition_expanded = pd.merge(complex_composition, multidatas, left_on='complex_multidata_id',
                                                right_on='id_multidata')

        complex_composition_expanded = pd.merge(complex_composition_expanded, multidatas,
                                                left_on='protein_multidata_id',
                                                right_on='id_multidata', suffixes=suffixes)

        return complex_composition_expanded

    def get_complex_by_multidatas(self, multidatas: pd.DataFrame, all_proteins_expressed: bool = True) -> pd.DataFrame:
        complex_composition = self.get_all_compositions()

        multidatas_ids = multidatas['id_multidata'].to_frame()
        complex_composition_merged = pd.merge(complex_composition, multidatas_ids, left_on='protein_multidata_id',
                                              right_on='id_multidata')

        if complex_composition_merged.empty:
            return complex_composition_merged

        def all_protein_expressed(complex):
            number_proteins_in_counts = len(
                complex_composition_merged[
                    complex_composition_merged['complex_multidata_id'] == complex['complex_multidata_id']])

            if number_proteins_in_counts < complex['total_protein']:
                return False

            return True

        if all_proteins_expressed:
            complex_composition_merged = complex_composition_merged[
                complex_composition_merged.apply(all_protein_expressed, axis=1)]

        complexes = self.get_all_expanded()
        complex_composition_merged = pd.merge(complex_composition_merged, complexes,
                                              left_on='complex_multidata_id',
                                              right_on='id_multidata',
                                              suffixes=['_protein', ''])

        complex_composition_merged.drop_duplicates(['complex_multidata_id'], inplace=True)

        return complex_composition_merged
