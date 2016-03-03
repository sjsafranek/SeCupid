#!/usr/bin/env python

import builtins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
        builtins.DATABASE_PATH,
        convert_unicode=True,
        echo=False
    )

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """ initiate database """
    import Models
    Base.metadata.create_all(bind=engine)
