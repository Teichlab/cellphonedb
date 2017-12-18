import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models.complex_composition.db_model_complex_composition import ComplexComposition


def get_all():
    """

    :rtype: pd.DataFrame
    """
    complex_composition_query = db.session.query(ComplexComposition.protein_multidata_id,
                                                 ComplexComposition.complex_multidata_id,
                                                 ComplexComposition.total_protein)
    complex_composition = pd.read_sql(complex_composition_query.statement, db.engine)

    return complex_composition
