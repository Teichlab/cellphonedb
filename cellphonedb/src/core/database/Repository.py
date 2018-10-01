import pandas as pd

from cellphonedb.src.core.core_logger import core_logger
from cellphonedb.src.core.database import DatabaseManager


class Repository():
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # TODO: Needs refactor
    @staticmethod
    def _blend_column(original_df: pd.DataFrame, multidata_df: pd.DataFrame, original_column_name: list,
                      db_column_name: list,
                      table_name: str, number: int) -> pd.DataFrame:
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

    # TODO: Needs refactor
    @staticmethod
    def blend_dataframes(left_df, left_column_names, right_df, db_column_name, db_table_name, quiet=False):
        result_df = left_df.copy()

        if not quiet and db_column_name in left_df.columns:
            core_logger.debug('WARNING | BLENDING: column "%s" already exists in orginal df' % (db_column_name))

        unique_slug = '_EDITNAME'
        unique_original_column_names = [("%s%s" % (column_name, unique_slug)) for column_name in left_column_names]

        result_df.rename(index=str, columns=dict(zip(left_column_names, unique_original_column_names)),
                         inplace=True)

        not_existent_proteins = []

        for i in range(0, len(unique_original_column_names)):
            result_df = Repository._blend_column(result_df, right_df, unique_original_column_names[i],
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
            core_logger.warning('WARNING | BLENDING: THIS %s DIDNT EXIST IN %s' % (db_column_name, db_table_name))
            core_logger.warning(not_existent_proteins)

        return result_df
