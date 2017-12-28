import pandas as pd

from cellphonedb.extensions import db
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein


def get_all():
    protein_query = db.session.query(Protein, Multidata).join(Multidata)
    protein = pd.read_sql(protein_query.statement, db.session.bind)

    return protein


def get_protein_multidata_by_uniprot(uniprot):
    """

    :type uniprot: str
    :rtype: pd.Series
    """
    protein_query = db.session.query(Protein, Multidata).join(Multidata).filter_by(name=uniprot).limit(1)
    protein = pd.read_sql(protein_query.statement, db.session.bind)

    if not protein.empty:
        return protein.iloc[0, :]
    return None
