from sqlalchemy import Column, Integer, ForeignKey

from cellphonedb.src.core.database.sqlalchemy_models import Base


class ComplexComposition(Base):
    __tablename__ = 'complex_composition_table'
    id_complex_composition = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = Column(Integer, ForeignKey('multidata_table.id_multidata'), nullable=False)
    protein_multidata_id = Column(Integer, ForeignKey('multidata_table.id_multidata'), nullable=False)
    total_protein = Column(Integer)
