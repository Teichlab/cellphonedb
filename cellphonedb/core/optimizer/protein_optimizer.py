import pandas as pd

from cellphonedb.core.exporters import protein_exporter
from cellphonedb.core.models.multidata.properties_multidata import is_cellphone_ligand


def call(multidatas: pd.DataFrame, interactions: pd.DataFrame):
    multidatas['is_cellphone_ligand'] = multidatas.apply(
        lambda multidata: is_cellphone_ligand(multidata, interactions), axis=1)

    return protein_exporter.call(multidatas[multidatas['is_complex'] == False])
