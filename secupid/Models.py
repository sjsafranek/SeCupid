#!/usr/bin/python

from .Database import Base

import datetime
from sqlalchemy import ForeignKey
# from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


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
    
    # questions
    lifestyle = Column(Integer, unique=False)
    dating = Column(Integer, unique=False)
    sex = Column(Integer, unique=False)
    other = Column(Integer, unique=False)
    ethics = Column(Integer, unique=False)
    religion = Column(Integer, unique=False)

    # info
    basics = Column(String(150), unique=False)
    background = Column(String(150), unique=False)
    misc = Column(String(150), unique=False)
    looking_for = Column(String(150), unique=False)

    # personality traits
    traits = Column(String(150), unique=False)

    # messaged
    messaged = Column(Boolean, unique=False)
    messaged_date = Column(DateTime, unique=False)

    active = Column(Boolean, unique=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", backref="profiles")

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % (self.username)


class Profile(Base):
    """ profile table """
    __tablename__ = 'profiles'
    uuid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    user_id = Column(Integer, ForeignKey('users.uuid'))
    source = Column(String, unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % (self.username)
