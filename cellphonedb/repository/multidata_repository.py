import pandas as pd

from cellphonedb.extensions import db
from cellphonedb.models.complex.db_model_complex import Complex
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


def get_all():
    query = db.session.query(Multidata)
    result = pd.read_sql(query.statement, db.engine)

    return result


def get_all_expanded():
    query_single = db.session.query(Gene, Protein, Multidata).join(Protein).join(Multidata)
    multidata_simple = pd.read_sql(query_single.statement, db.engine)

    query_complex = db.session.query(Multidata, Complex).join(Complex)
    multidata_complex = pd.read_sql(query_complex.statement, db.engine)

    multidata_expanded = multidata_simple.append(multidata_complex, ignore_index=True)

    return multidata_expanded


def get_multidatas_from_string(input_string: str) -> pd.DataFrame:
    multidatas = get_all_expanded()

    return multidatas[(multidatas['name'] == input_string) |
                      (multidatas['ensembl'] == input_string) |
                      (multidatas['entry_name'] == input_string) |
                      (multidatas['gene_name'] == input_string) |
                      (multidatas['ensembl'] == input_string)]
