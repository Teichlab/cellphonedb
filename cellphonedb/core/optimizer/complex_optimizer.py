import pandas as pd

from cellphonedb.core.exporters import complex_exporter
from cellphonedb.core.models.multidata.properties_multidata import is_cellphone_ligand
from cellphonedb.core.utils import filters


def call(multidatas: pd.DataFrame, interactions: pd.DataFrame, multidata_column_names, complexes, complex_compositions,
         proteins):
    multidatas['is_cellphone_ligand'] = multidatas.apply(
        lambda multidata: is_cellphone_ligand(multidata, interactions), axis=1)

    multidatas_for_complex = filters.remove_not_defined_columns(multidatas, multidata_column_names)

    return complex_exporter.call(complexes, multidatas_for_complex, complex_compositions, proteins)
