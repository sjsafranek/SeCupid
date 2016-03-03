#!/usr/bin/python

# OkCupid_Se

import os
import time
import builtins
import Conf
import Models
import Database
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains


class SeCupid(object):
	""" Selenium Handler for OkCupid """

	def __init__(self, username, password):
		""" Initiate SeCupid Class
			Args:
				username (str): OkCupid username
				password (str): OkCupid password
		"""
		# setup database
		Database.init_db()
		Session = sessionmaker(bind=Database.engine)
		self.session = Session()
		# Setup browser
		self.username = username
		self.password = password
		# self.driver = webdriver.Firefox()
		self.driver = webdriver.PhantomJS("phantomjs-2.0.0-linux/phantomjs")
		self.driver.implicitly_wait(10)
		#
		self.update = False
		self.scrape = True

	def _cancelLoading(self):
		"""Cancels loading web page"""
		print("cancel loading...")
		self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

	def login(self):
		""" Log into OkCupid account """
		url = "https://www.okcupid.com/login"
		print(url)
		self.driver.get(url)
		self.driver.find_element(By.ID, "login_username").send_keys(self.username)
		self.driver.find_element(By.ID, "login_password").send_keys(self.password)
		self.driver.find_element(By.ID, "sign_in_button").click()
		time.sleep(2)
		self._cancelLoading()

	def _load_all_users(self, numTimes=10000):
		""" Cancels loading web page """
		print("loading users...")
		lastNum = 0
		newNum = 1
		num = 0
		while lastNum != newNum and num < numTimes:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(.75)
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(.75)
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(5)
			lastNum = newNum
			profile_boxes = self.driver.find_elements(By.CLASS_NAME, "profile_info")
			num += 1
			newNum = len(profile_boxes)

	def takeScreenShot(self, filename):
		""" Takes screenshot and saves to png
			Args:
				filename (str): save file for screenshot
		"""
		self.driver.save_screenshot(str(filename) + '.png')

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

	def getAllUsers(self):
		""" Scrapes `/match` page for user profiles """
		url = "http://www.okcupid.com/match"
		print(url)
		self.driver.get(url)
		time.sleep(5)
		self.scrape = False
		self._cancelLoading()
		self._load_all_users()
		users = self.driver.find_elements(By.CLASS_NAME, "match_card_text")
		for user in users:
			username = user.find_element(By.CLASS_NAME, "username").text
			try:
				# Age
				age = user.find_element(By.CLASS_NAME, "age").text
				if age == "-":
					age = 0
				else:
					age = int(age)
				# Location
				location = user.find_element(By.CLASS_NAME, "location").text
				# Match
				match_wrapper = user.find_element(By.CSS_SELECTOR, "div.percentage_wrapper.match")
				match = match_wrapper.find_element(By.CLASS_NAME, "percentage").text
				match = match.replace("%","")
				if match == "—":
					match = 0
				else:
					match = int(match)
				# Enemy
				enemy_wrapper = user.find_element(By.CSS_SELECTOR, "div.percentage_wrapper.enemy")
				enemy = enemy_wrapper.find_element(By.CLASS_NAME, "percentage").text
				enemy = enemy.replace("%","")
				if enemy == "—":
					enemy = 0
				else:
					enemy = int(enemy)
				# Like status
				liked = False
				try:
					rating_liked = user.find_element(By.CLASS_NAME, "rating_liked")
					liked = True
				except NoSuchElementException:
					rating_like = user.find_element(By.CLASS_NAME, "rating_like")
					liked = False
				self.newUser(username, age, location, match, enemy, liked)
			except Exception as e:
				self.takeScreenShot(time.time())
				print(e)
				traceback.print_stack()
				time.sleep(360)

	def visitProfile(self, username):
		""" Visits the profile page of a user
			Args:
				username (str): OkCupid username
		"""
		url = "http://www.okcupid.com/profile/%s" % username
		self.driver.get(url)
		time.sleep(5)

