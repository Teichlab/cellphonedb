from sqlalchemy import Column, Integer, Float, String, ForeignKey

from cellphonedb.models import Base


class Interaction(Base):
    __tablename__ = 'interaction'

    id_interaction = Column(Integer, nullable=False, primary_key=True)

    multidata_1_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False)
    multidata_2_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False)

    score_1 = Column(Float)
    score_2 = Column(Float)

    source = Column(String)
    comments = Column(String)
