from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from cellphonedb.core.database.sqlalchemy_models import Base


class Multidata(Base):
    __tablename__ = 'multidata'
    id_multidata = Column(Integer, nullable=False, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    receptor = Column(Boolean)
    receptor_desc = Column(String)
    adhesion = Column(Boolean)
    other = Column(Boolean)
    other_desc = Column(String)
    transporter = Column(Boolean)
    secreted_highlight = Column(Boolean)
    secreted_desc = Column(String)
    transmembrane = Column(Boolean)
    secretion = Column(Boolean)
    peripheral = Column(Boolean)
    cytoplasm = Column(Boolean)
    extracellular = Column(Boolean)
    integrin_interaction = Column(Boolean)
    is_complex = Column(Boolean)

    protein = relationship('Protein', backref='protein', lazy='subquery')
    complex = relationship('Complex', backref='complex', lazy='subquery')
