from sqlalchemy import Column, Integer, String, ForeignKey

from cellphonedb.src.core.database.sqlalchemy_models import Base


class Complex(Base):
    __tablename__ = 'complex_table'
    id_complex = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = Column(Integer, ForeignKey('multidata_table.id_multidata'), nullable=False, unique=True)
    pdb_structure = Column(String)
    pdb_id = Column(String)
    stoichiometry = Column(String)
    comments_complex = Column(String)
