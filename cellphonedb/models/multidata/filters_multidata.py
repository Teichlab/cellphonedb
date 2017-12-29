import pandas as pd


def filter_by_lingand_or_receptor(multidatas: pd.DataFrame) -> pd.DataFrame:
    result = multidatas[
        multidatas[['is_cellphone_ligand', 'is_cellphone_receptor']].apply(lambda multidata: multidata.any(), axis=1)]

    return result
