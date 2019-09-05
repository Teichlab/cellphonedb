from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from cellphonedb.src.core.database.sqlalchemy_models import Base


class Protein(Base):
    __tablename__ = 'protein_table'
    id_protein = Column(Integer, nullable=False, primary_key=True)

    protein_name = Column(String)
    tags = Column(String)
    tags_reason = Column(String)
    tags_description = Column(String)
    # pfam = Column(String)

    protein_multidata_id = Column(Integer, ForeignKey('multidata_table.id_multidata'), unique=True, nullable=False)
    gene = relationship('Gene', backref='gene_table', lazy='subquery')
