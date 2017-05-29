from sqlalchemy import Column, String, Integer, ForeignKey, Float, Binary, \
    Boolean, UniqueConstraint, Table

from cellcommdb.extensions import db


class IdModel(object):
    id = Column(Integer, nullable=False, primary_key=True)


class Multidata(db.Model, IdModel):
    __tablename__ = 'multidata'

    name = Column(String, nullable=False, unique=True)

    receptor = Column(Boolean)
    receptor_highlight = Column(Boolean)
    receptor_desc = Column(String)
    adhesion = Column(Boolean)
    other = Column(Boolean)
    other_desc = Column(String)
    transporter = Column(Boolean)
    secreted_highlight = Column(Boolean)
    secreted_desc = Column(String)
    comments = Column(String)

    # protein = db.relationship('Protein', backref='multidata', lazy='joined')


class Protein(db.Model, IdModel):
    __tablename__ = 'protein'

    entry_name = Column(String)
    transmembrane = Column(Boolean)
    secretion = Column(Boolean)
    peripheral = Column(Boolean)
    tags = Column(String)
    tags_reason = Column(String)

    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), unique=True, nullable=False)


class Complex_composition(db.Model, IdModel):
    __tablename__ = 'complex_composition'

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False)
    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False)


class Complex(db.Model, IdModel):
    __tablename__ = 'complex'

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False, unique=True)
    pdb_structure = Column(Boolean)
    pdb_id = Column(String)
    stoichiometry = Column(String)
    comments = Column(String)


# TODO: Delete me
# class Gene(db.Model, IdModel):
#     __tablename__ = "gene"
#
#     ensembl = Column(String)
#     name = Column(String)
#
#     protein_id = Column(Integer, ForeignKey('protein.id'))
#
#     protein = db.relationship('Protein', backref=db.backref('protein'))





#
# complex_composition_table = Table(
#     'complex_composition', db.metadata,
#     Column('complex_id', Integer, ForeignKey('complex.id')),
#     Column('protein_id', Integer, ForeignKey('protein.id')),
#     Column('stoichiometry', Integer)
# )
