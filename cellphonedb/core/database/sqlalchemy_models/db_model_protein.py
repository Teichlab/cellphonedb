from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from cellphonedb.core.database.sqlalchemy_models import Base


class Protein(Base):
    __tablename__ = 'protein'
    id_protein = Column(Integer, nullable=False, primary_key=True)

    entry_name = Column(String)
    tags = Column(String)
    tags_reason = Column(String)
    tags_description = Column(String)

    protein_multidata_id = Column(Integer, ForeignKey('multidata.id_multidata'), unique=True, nullable=False)
    gene = relationship('Gene', backref='gene', lazy='subquery')
