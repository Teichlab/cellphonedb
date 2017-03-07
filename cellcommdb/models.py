from sqlalchemy import Column, String, Integer, ForeignKey, Float, Binary, \
    Boolean, UniqueConstraint

from cellcommdb.extensions import db


class IdModel(object):

    id = Column(Integer, nullable=False, primary_key=True)


class Gene(db.Model, IdModel):

    __tablename__ = "gene"

    ensembl = Column(String)
    name = Column(String)

    protein_id = Column(Integer, ForeignKey('protein.id'))

    protein = db.relationship('Protein', backref=db.backref('protein'))


class Protein(db.Model, IdModel):

    __tablename__ = "protein"

    uniprot = Column(String, nullable=False)
    entry_name = Column(String)

    transmembrane = Column(Boolean)
    secretion = Column(Boolean)
    peripheral = Column(Boolean)
    receptor = Column(Boolean)
    receptor_highlight = Column(Boolean)
    receptor_desc = Column(String)
    adhesion = Column(Boolean)
    other = Column(Boolean)
    other_desc = Column(String)
    transporter = Column(Boolean)
    secreted_highlight = Column(Boolean)
    secreted_desc = Column(String)
    tags = Column(String)
    tags_reason = Column(String)
