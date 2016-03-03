#!/usr/bin/python

from Database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship, backref

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

