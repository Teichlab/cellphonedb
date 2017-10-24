import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models import Multidata
from cellcommdb.tools.filters import remove_not_defined_columns


class Unblend:
    @staticmethod
    def unblend_column(original_df, original_name_column, data_df, target_name_column, result_name_column):

        result = pd.merge(original_df, data_df, left_on=original_name_column, right_on='id', how='left')
        result.rename(index=str,
                      columns={target_name_column: result_name_column},
                      inplace=True)

        return result

    @staticmethod
    def multidata(original_df, columns_to_merge, result_name_base, remove_original=False):
        multidata_query = db.session.query(Multidata.id, Multidata.name)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)

        target_name_column = 'name'
        result_name_columns = [('%s_%s' % (result_name_base, i + 1)) for i in range(len(columns_to_merge))]

        result = original_df.copy()

        for index in range(len(columns_to_merge)):
            result = Unblend.unblend_column(result, columns_to_merge[index], multidata_df, target_name_column,
                                            result_name_columns[index])
            remove_not_defined_columns(result, list(original_df.columns.values) + result_name_columns)

        if remove_original:
            result.drop(columns_to_merge, inplace=True, axis=1)

        return result
