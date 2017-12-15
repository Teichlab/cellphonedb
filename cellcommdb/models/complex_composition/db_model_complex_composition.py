from sqlalchemy import Column, Integer

from cellcommdb.extensions import db


class ComplexComposition(db.Model):
    __tablename__ = 'complex_composition'
    id_complex_composition = Column(Integer, nullable=False, primary_key=True)

    complex_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)
    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)
    total_protein = Column(Integer)
