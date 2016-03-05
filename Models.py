#!/usr/bin/python

# from Database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship, backref


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



class User(Base):
    """ users table """
    __tablename__ = 'users'
    uuid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    location = Column(String(50), unique=False)
    age = Column(Integer, unique=False)
    match = Column(Float, unique=False)
    enemy = Column(Float, unique=False)
    liked = Column(Boolean, unique=False)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % (self.username)

