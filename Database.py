#!/usr/bin/env python

import Models
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
    # import Models
    Base.metadata.create_all(bind=engine)



class DB(object):
	""" Database for OkCupid Model Objects """

	def __init__(self, update=False):
		""" Create database connection """
		init_db()
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.update = update

	def getUser(self, username):
		""" Retrieves user from database
			Args:
				username (str): OkCupid username
			Returns:
				User object if username is in database
				None if username not in database
		"""
		user = self.session.query(Models.User).filter(Models.User.username==username).first()
		return user

	def newUser(self, username, age, location, match, enemy, liked):
		""" Adds user to database
			Args:
				username (str): OkCupid username
				age (int): age of user
				match (float): match percentage
				liked (bool): Whether user has been `liked`
		"""
		user = self.getUser(username)
		if not user:
			print("Inserting new user:", username)
			self.scrape = True
			try:
				user = Models.User(username)
				user.age = age
				user.location = location
				user.match = match
				user.enemy = enemy
				user.liked = liked
				self.session.add(user)
				self.session.commit()
			except Exception as e:
				print(e)
				traceback.print_stack()
				self.session.rollback()
		elif self.update:
			print("Update existing user:", username)
			try:
				user.age = age
				user.location = location
				user.match = match
				user.enemy = enemy
				user.liked = liked
				self.session.commit()
			except Exception as e:
				print(e)
				traceback.print_stack()
				self.session.rollback()
		else:
			print("User already exisits:", username)

	def getUsersFromDB(self):
		""" Retrieves all user records from database
			Returns:
				users list(Models.User): list of User model objects 
		"""
		users = self.session.query(Models.User).all()
		return users

	def getLikedUsersFromDB(self):
		""" Retrieves liked user records from database
			Returns:
				users list(Models.User): list of User model objects 
		"""
		users = self.session.query(Models.User).filter(Models.User.liked==True).all()
		return users

