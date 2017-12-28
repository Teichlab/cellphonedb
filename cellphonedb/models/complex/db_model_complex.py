from sqlalchemy import Column, Integer, String

from cellphonedb.extensions import db


class Complex(db.Model):
    __tablename__ = 'complex'
    id_complex = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False, unique=True)
    pdb_structure = Column(String)
    pdb_id = Column(String)
    stoichiometry = Column(String)
    comments = Column(String)
