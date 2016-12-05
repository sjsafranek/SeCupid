#!/usr/bin/env python

from .Conf import *
from .utils.ligneous import log

import lzma
import base64
import builtins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
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

from .Models import *


class Database(object):
	""" Database for OkCupid Model Objects """

	def __init__(self, update=False):
		""" Create database connection """
		self._init_db()
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.update = update
		self.logger = log("DB")

	def _init_db(self):
		""" initiate database """
		Base.metadata.create_all(bind=engine)

	def getUser(self, username):
		""" Retrieves user from database
			Args:
				username (str): OkCupid username
			Returns:
				User object if username is in database
				None if username not in database
		"""
		user = self.session.query(User).filter(User.username==username).first()
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
			self.logger.info("Insert: " + username)
			try:
				user = User(username)
				user.age = age
				user.location = location
				user.match = match
				user.enemy = enemy
				user.liked = liked
				self.session.add(user)
				self.session.commit()
				return True
			except Exception as e:
				self.logger.error(e)
				traceback.print_stack()
				self.session.rollback()
				return False
		elif self.update:
			self.logger.info("Update: " + username)
			try:
				user.age = age
				user.location = location
				user.match = match
				user.enemy = enemy
				user.liked = liked
				self.session.commit()
				return False
			except Exception as e:
				self.logger.error(e)
				traceback.print_stack()
				self.session.rollback()
				return False
		#else:
		#	self.logger.info("User already exisits:", username)

	def getUsers(self):
		""" Retrieves all user records from database
			Returns:
				users list(Models.User): list of User model objects 
		"""
		users = self.session.query(User).all()
		return users

	def getLikedUsers(self):
		""" Retrieves liked user records from database
			Returns:
				users list(Models.User): list of User model objects 
		"""
		users = self.session.query(User).filter(User.liked==True).all()
		return users

	def getProfile(self, username):
		""" Gets user profile from profiles table
			Args:
				username (str): okcupid username
			Returns:
				profile (str): okcupid profile html source
		"""
		profile = self.session.query(Models.Profile).filter(Models.Profile.username == username).first()
		return profile
		# if profile:
		# 	udatab64 = base64.b64decode(profile.source)
		# 	decoded = lzma.decompress(udatab64)
		# 	return decoded
		# else:
		# 	return None

	def saveProfile(self, username, profile_source):
		""" Save profile to database. 
			Profile linked to user in users table.
			Args:
				username (str): okcupid username
				profile_source (str): html source of profile page
		"""
		data = lzma.compress(profile_source.encode())
		encoded = base64.b64encode(data).decode('utf-8')
		profile = self.getProfile(username)
		if not profile:
			self.logger.info("Creating profile: %s" % username)
			profile = Models.Profile(username)
			self.session.add(profile)
			self.session.commit()
			profile.source = encoded
			self.session.commit()
			user = self.getUser(username)
			if not user:
				user = User(username)
				self.session.add(user)
				self.session.commit()
			user.profile.append(profile)
			self.session.commit()
		# elif self.update:
		else:
			self.logger.info("Updating profile: %s" % username)
			profile.source = encoded
			self.session.commit()

	def decodeProfile(self, encoded):
		udatab64 = base64.b64decode(encoded)
		decoded = lzma.decompress(udatab64)
		return decoded

