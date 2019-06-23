from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from cellphonedb.src.core.database.sqlalchemy_models import Base


class Multidata(Base):
    __tablename__ = 'multidata_table'
    id_multidata = Column(Integer, nullable=False, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    receptor = Column(Boolean)
    receptor_desc = Column(String)
    other = Column(Boolean)
    other_desc = Column(String)
    secreted_highlight = Column(Boolean)
    secreted_desc = Column(String)
    transmembrane = Column(Boolean)
    secreted = Column(Boolean)
    peripheral = Column(Boolean)
    integrin = Column(Boolean)
    is_complex = Column(Boolean)

    protein = relationship('Protein', backref='protein_table', lazy='subquery')
    complex = relationship('Complex', backref='complex_table', lazy='subquery')
