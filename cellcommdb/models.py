from sqlalchemy import Column, String, Integer, ForeignKey, Float, Binary, \
    Boolean, UniqueConstraint, Table, Enum

from cellcommdb.extensions import db


class Multidata(db.Model):
    __tablename__ = 'multidata'
    id_multidata = Column(Integer, nullable=False, primary_key=True)

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
    transmembrane = Column(Boolean)
    secretion = Column(Boolean)
    peripheral = Column(Boolean)
    ligand = Column(Boolean)
    cytoplasm = Column(Boolean)
    extracellular = Column(Boolean)

    protein = db.relationship('Protein', backref='protein', lazy='subquery')
    complex = db.relationship('Complex', backref='complex', lazy='subquery')


class Protein(db.Model):
    __tablename__ = 'protein'
    id_protein = Column(Integer, nullable=False, primary_key=True)

    entry_name = Column(String)
    tags = Column(String)
    tags_reason = Column(String)

    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), unique=True, nullable=False)
    gene = db.relationship('Gene', backref='gene', lazy='subquery')


class ComplexComposition(db.Model):
    __tablename__ = 'complex_composition'
    id_complex_composition = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)
    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)
    total_protein = Column(Integer)


class Complex(db.Model):
    __tablename__ = 'complex'
    id_complex = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False, unique=True)
    pdb_structure = Column(String)
    pdb_id = Column(String)
    stoichiometry = Column(String)
    comments = Column(String)


class Interaction(db.Model):
    __tablename__ = 'interaction'

    id_interaction = Column(Integer, nullable=False, primary_key=True)

    multidata_1_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)
    multidata_2_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)

    score_1 = db.Column(Float)
    score_2 = db.Column(Float)

    source = db.Column(String)
    comments = db.Column(String)


class Gene(db.Model):
    __tablename__ = 'gene'
    id_gene = Column(Integer, nullable=False, primary_key=True)

    ensembl = Column(String, nullable=False)
    gene_name = Column(String, nullable=False)

    protein_id = Column(Integer, ForeignKey('protein.id_protein'))
