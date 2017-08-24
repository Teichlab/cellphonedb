import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models import Multidata


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
        interaction_df.rename(index=str, columns={'id': '%s_%s_id' % (table_name, number)}, inplace=True)

        interaction_df = interaction_df[
            (interaction_df['_merge'] == 'both') | (interaction_df['_merge'] == 'left_only')]
        interaction_df.rename(index=str,
                              columns={'_merge': '_merge_%s' % number, db_column_name: db_column_name + '_%s' % number},
                              inplace=True)

        return interaction_df

    @staticmethod
    def blend_multidata(original_df, original_column_names):
        """
        Merges dataframe with multidata names in multidata ids
        :type original_df: pd.DataFrame
        :type original_column_names: list
        :type result_column_names: list
        :return:
        """
        multidata_query = db.session.query(Multidata.id, Multidata.name)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)

        db_column_name = 'name'

        interaction_df = original_df.drop('id', errors='ignore')

        not_existent_proteins = []

        for i in range(0, len(original_column_names)):
            interaction_df = Blend._blend_column(interaction_df, multidata_df, original_column_names[i], db_column_name,
                                           'multidata', i + 1)

            not_existent_proteins = not_existent_proteins + \
                                    interaction_df[interaction_df['_merge_%s' % (i + 1)] == 'left_only'][
                                        original_column_names[i]].drop_duplicates().tolist()
        not_existent_proteins = list(set(not_existent_proteins))

        for i in range(1, len(original_column_names) + 1):
            interaction_df = interaction_df[(interaction_df['_merge_%s' % i] == 'both')]

        interaction_df.drop(['_merge_%s' % merge_column for merge_column in
                             range(1, len(original_column_names) + 1)] + original_column_names, axis=1, inplace=True)

        if not_existent_proteins:
            print('WARNING | BLENDING INTERACTIONS-MULTIDATA: THIS PROTEINS DIDNT EXIST IN DATABASE')
            print(not_existent_proteins)

        return interaction_df
