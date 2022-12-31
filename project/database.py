from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app


Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = create_engine(current_app.config['DATABASE'])
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=self.engine))

        Base.objects = self.db_session.query_property()

        import project.models as models  # noqa
        Base.metadata.create_all(bind=self.engine)
