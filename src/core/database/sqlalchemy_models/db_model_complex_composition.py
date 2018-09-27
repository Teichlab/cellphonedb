from sqlalchemy import Column, Integer, ForeignKey

from src.core.database.sqlalchemy_models import Base


class ComplexComposition(Base):
    __tablename__ = 'complex_composition'
    id_complex_composition = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False)
    protein_multidata_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False)
    total_protein = Column(Integer)
