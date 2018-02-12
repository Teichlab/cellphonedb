from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, engine):
        self.engine = engine
        self.established_session = None
        self.base = declarative_base()
        self.base_model = None

    @property
    def session(self):
        if not self.established_session:
            session = sessionmaker(bind=self.engine)
            self.established_session = session()

        return self.established_session
