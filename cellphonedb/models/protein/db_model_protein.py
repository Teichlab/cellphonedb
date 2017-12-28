from sqlalchemy import Column, Integer, String

from cellphonedb.extensions import db


class Protein(db.Model):
    __tablename__ = 'protein'
    id_protein = Column(Integer, nullable=False, primary_key=True)

    entry_name = Column(String)
    tags = Column(String)
    tags_reason = Column(String)

    protein_multidata_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), unique=True, nullable=False)
    gene = db.relationship('Gene', backref='gene', lazy='subquery')
