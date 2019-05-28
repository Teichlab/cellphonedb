from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from cellphonedb.src.core.database.sqlalchemy_models import Base


class Interaction(Base):
    __tablename__ = 'interaction'

    id_interaction = Column(Integer, nullable=False, primary_key=True)
    id_cp_interaction = Column(String, nullable=False, unique=True)

    multidata_1_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False)
    multidata_2_id = Column(Integer, ForeignKey('multidata.id_multidata'), nullable=False)


    source = Column(String)
    comments_interaction = Column(String)

    is_cellphonedb_interactor = Column(Boolean)
