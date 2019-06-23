from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from cellphonedb.src.core.database.sqlalchemy_models import Base


class Interaction(Base):
    __tablename__ = 'interaction_table'

    id_interaction = Column(Integer, nullable=False, primary_key=True)
    id_cp_interaction = Column(String, nullable=False, unique=True)

    multidata_1_id = Column(Integer, ForeignKey('multidata_table.id_multidata'), nullable=False)
    multidata_2_id = Column(Integer, ForeignKey('multidata_table.id_multidata'), nullable=False)

    source = Column(String)
    annotation_strategy = Column(String)
