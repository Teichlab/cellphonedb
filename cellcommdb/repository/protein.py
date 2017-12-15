import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models import Multidata, Protein


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
