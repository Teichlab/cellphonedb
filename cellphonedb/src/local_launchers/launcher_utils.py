import pandas as pd

from cellphonedb.utils import utils


def read_meta_file(path, filename):
    meta_raw = utils.read_data_table_from_file('{}/{}'.format(path, filename), index_column_first=True)
    meta = pd.DataFrame(index=meta_raw.index)
    meta['cell_type'] = meta_raw.iloc[:, 0]
    return meta
