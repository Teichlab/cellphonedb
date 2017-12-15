from sqlalchemy import Column, Integer, Float, String

from cellcommdb.extensions import db


class Interaction(db.Model):
    __tablename__ = 'interaction'

    id_interaction = Column(Integer, nullable=False, primary_key=True)

    multidata_1_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)
    multidata_2_id = db.Column(db.Integer, db.ForeignKey('multidata.id_multidata'), nullable=False)

    score_1 = db.Column(Float)
    score_2 = db.Column(Float)

    source = db.Column(String)
    comments = db.Column(String)
