from sqlalchemy import MetaData, ForeignKeyConstraint, Table
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import DropConstraint, DropTable


# TODO: create sqlalchemy inheritance
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

    def create_all(self):
        self.base_model.metadata.create_all(self.engine)

    def drop_everything(self):
        conn = self.engine.connect()

        trans = conn.begin()

        inspector = reflection.Inspector.from_engine(self.engine)

        metadata = MetaData()

        tbs = []
        all_fks = []

        for table_name in inspector.get_table_names():
            fks = []
            for fk in inspector.get_foreign_keys(table_name):
                if not fk['name']:
                    continue
                fks.append(
                    ForeignKeyConstraint((), (), name=fk['name'])
                )
            t = Table(table_name, metadata, *fks)
            tbs.append(t)
            all_fks.extend(fks)

        for fkc in all_fks:
            conn.execute(DropConstraint(fkc))

        for table in tbs:
            conn.execute(DropTable(table))

        trans.commit()
