import pandas as pd

from cellphonedb.extensions import db
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


def get_all():
    query = db.session.query(Gene)
    result = pd.read_sql(query.statement, db.session.bind)

    return result


def get_all_expanded():
    query = db.session.query(Gene, Protein, Multidata).join(Protein).join(Multidata)
    result = pd.read_sql(query.statement, db.session.bind)

    return result
