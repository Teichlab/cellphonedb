import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models.multidata.db_model_multidata import Multidata
from cellcommdb.models.protein.db_model_protein import Protein


class Blend:
    @staticmethod
    def _blend_column(original_df, multidata_df, original_column_name, db_column_name,
                      table_name, number):
        """

        :type original_df: pd.DataFrame
        :type multidata_df: pd.DataFrame
        :type original_column_name: str
        :type db_column_name: str
        :type table_name: str
        :type number: int
        :rtype: pd.DataFrame
        """
        interaction_df = pd.merge(original_df, multidata_df, left_on=original_column_name, right_on=db_column_name,
                                  indicator=True, how='outer')
        interaction_df.rename(index=str, columns={'id_%s' % table_name: '%s_%s_id' % (table_name, number)},
                              inplace=True)

        interaction_df = interaction_df[
            (interaction_df['_merge'] == 'both') | (interaction_df['_merge'] == 'left_only')]
        interaction_df.rename(index=str,
                              columns={'_merge': '_merge_%s' % number, db_column_name: db_column_name + '_%s' % number},
                              inplace=True)

        return interaction_df

    @staticmethod
    def blend_multidata(original_df, original_column_names, quiet=False):
        """
        Merges dataframe with multidata names in multidata ids
        :type original_df: pd.DataFrame
        :type original_column_names: list
        :type quiet: bool
        :rtype: pd.DataFrame
        """
        if quiet:
            print('Blending proteins in quiet mode')
        multidata_query = db.session.query(Multidata.id_multidata, Multidata.name)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)

        result = Blend.blend_dataframes(original_df, original_column_names, multidata_df, 'name', 'multidata')

        return result

    @staticmethod
    def blend_dataframes(left_df, left_column_names, right_df, db_column_name, db_table_name, quiet=False):
        result_df = left_df.drop('id', errors='ignore', axis=1)

        if not quiet and db_column_name in left_df.columns:
            print('WARNING | BLENDING: column "%s" already exists in orginal df' % (db_column_name))

        unique_slug = '_EDITNAME'
        unique_original_column_names = [("%s%s" % (column_name, unique_slug)) for column_name in left_column_names]

        result_df.rename(index=str, columns=dict(zip(left_column_names, unique_original_column_names)),
                         inplace=True)

        not_existent_proteins = []

        for i in range(0, len(unique_original_column_names)):
            result_df = Blend._blend_column(result_df, right_df, unique_original_column_names[i],
                                            db_column_name,
                                            db_table_name, i + 1)

            not_existent_proteins = not_existent_proteins + \
                                    result_df[result_df['_merge_%s' % (i + 1)] == 'left_only'][
                                        unique_original_column_names[i]].drop_duplicates().tolist()
        not_existent_proteins = list(set(not_existent_proteins))

        for i in range(1, len(unique_original_column_names) + 1):
            result_df = result_df[(result_df['_merge_%s' % i] == 'both')]

        result_df.drop(['_merge_%s' % merge_column for merge_column in
                        range(1, len(unique_original_column_names) + 1)] + unique_original_column_names, axis=1,
                       inplace=True)

        if len(left_column_names) == 1:
            result_df.rename(index=str, columns={'%s_1' % db_column_name: db_column_name,
                                                 '%s_1_id' % db_table_name: '%s_id' % db_table_name}, inplace=True)

        if not quiet and not_existent_proteins:
            print('WARNING | BLENDING: THIS %s DIDNT EXIST IN %s' % (db_column_name, db_table_name))
            print(not_existent_proteins)

        return result_df

    @staticmethod
    def blend_protein(original_df, original_column_names, quiet=False):
        if quiet:
            print('Blending proteins in quiet mode')
        database_query = db.session.query(Protein.id_protein, Multidata.name).join(Multidata)
        database_df = pd.read_sql(database_query.statement, db.engine)

        protein_df = Blend.blend_dataframes(original_df, original_column_names, database_df, 'name', 'protein',
                                            quiet=quiet)

        return protein_df
