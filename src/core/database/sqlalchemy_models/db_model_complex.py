from sqlalchemy import Column, Integer, String, ForeignKey

from src.core.database.sqlalchemy_models import Base


class Complex(Base):
    __tablename__ = 'complex'
    id_complex = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False, unique=True)
    pdb_structure = Column(String)
    pdb_id = Column(String)
    stoichiometry = Column(String)
    comments_complex = Column(String)
