from sqlalchemy import Column, String, Integer, ForeignKey, Float, Binary, \
    Boolean, UniqueConstraint, Table, Enum

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

    protein = db.relationship('Protein', backref='protein', lazy='subquery')
    complex = db.relationship('Complex', backref='complex', lazy='subquery')


class Protein(db.Model, IdModel):
    __tablename__ = 'protein'

    entry_name = Column(String)
    transmembrane = Column(Boolean)
    secretion = Column(Boolean)
    peripheral = Column(Boolean)
    tags = Column(String)
    tags_reason = Column(String)
    gene_name = Column(String)

    membrane_type = Column(String)

    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), unique=True, nullable=False)
    gene = db.relationship('Gene', backref='gene', lazy='subquery')


class Complex_composition(db.Model, IdModel):
    __tablename__ = 'complex_composition'

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False)
    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False)


class Complex(db.Model, IdModel):
    __tablename__ = 'complex'

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False, unique=True)
    pdb_structure = Column(String)
    pdb_id = Column(String)
    stoichiometry = Column(String)
    comments = Column(String)


class Unity_interaction(db.Model, IdModel):
    __tablename__ = 'unity_interaction'

    multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False, unique=True)
    source = db.Column(String)

class Interaction(db.Model, IdModel):
    __tablename__ = 'interaction'

    multidata_1_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False)
    multidata_2_id = db.Column(db.Integer, db.ForeignKey('multidata.id'), nullable=False)

    score_1 = db.Column(Float)
    score_2 = db.Column(Float)


class Gene(db.Model, IdModel):
    __tablename__ = 'gene'

    ensembl = Column(String, nullable=False)
    name = Column(String, nullable=False)
    mouse_uniprot = Column(String)
    mouse_ensembl = Column(String)

    protein_id = Column(Integer, ForeignKey('protein.id'))
