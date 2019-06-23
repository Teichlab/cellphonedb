from sqlalchemy import Column, Integer, String, ForeignKey

from cellphonedb.src.core.database.sqlalchemy_models import Base


class Gene(Base):
    __tablename__ = 'gene_table'
    id_gene = Column(Integer, nullable=False, primary_key=True)

    ensembl = Column(String, nullable=False)
    gene_name = Column(String, nullable=False)
    hgnc_symbol = Column(String)

    protein_id = Column(Integer, ForeignKey('protein_table.id_protein'), nullable=False)
