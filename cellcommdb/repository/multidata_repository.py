import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models.complex.db_model_complex import Complex
from cellcommdb.models.gene.db_model_gene import Gene
from cellcommdb.models.multidata.db_model_multidata import Multidata
from cellcommdb.models.protein.db_model_protein import Protein


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
