#!/usr/bin/python

__authors__ = ["Stefan Safranek"]
__copyright__ = "Copyright 2016, SeCupid"
__license__ = "MIT"
__version__ = "1.2.1"
__maintainer__ = "Stefan Safranek"
__email__ = "https://github.com/sjsafranek"
__status__ = "Development"
__date__ = "12/04/16"

#from .Conf import *
from .Database import Database
from .Error import DriverTypeError
from .utils.ligneous import log

import os
import time
import builtins
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains


class Browser(object):
	""" Selenium Driver Handler """
	def __init__(self, driver_type="firefox"):
		if "firefox" == driver_type:
			self.driver = webdriver.Firefox()
		elif "headless" == driver_type:
			self.driver = webdriver.PhantomJS("phantomjs-2.0.0-linux/phantomjs")
		elif "chrome"  == driver_type:
			self.driver = webdriver.Chrome("./chromedriver")
		else:
			# CREATE NEW ERROR TYPE
			raise DriverTypeError(driver_type, "chrome, firefox, headless")


class SeCupid(Browser):
	""" Selenium Handler for OkCupid """

	def __init__(self, username, password, driver_type):
		""" Initiate SeCupid Class
			Args:
				username (str): OkCupid username
				password (str): OkCupid password
		"""
		# setup database
		#self.db = Database.DB()
		self.db = Database()
		# Setup browser
		self.username = username
		self.password = password
		
		Browser.__init__(self, driver_type)

		self.driver.implicitly_wait(10)
		# options
		self.scrape = True
		# setup logging
		self.logger = log("SeCupid")

	def _cancelLoading(self):
		""" Cancels loading web page"""
		self.logger.info("cancel loading...")
		self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

	def login(self):
		""" Log into OkCupid account """
		url = "https://www.okcupid.com/login"
		self.logger.info(url)
		self.driver.get(url)
		self.driver.find_element(By.ID, "login_username").send_keys(self.username)
		self.driver.find_element(By.ID, "login_password").send_keys(self.password)
		self.driver.find_element(By.ID, "sign_in_button").click()
		if "Your info was incorrect. Try again." in self.driver.find_element(By.TAG_NAME, "body").text:
			self.driver.quit()
			raise ValueError("Your info was incorrect. Try again.")
		time.sleep(2)
		self._cancelLoading()

	def _load_all_users(self, numTimes=10000):
		""" Cancels loading web page """
		self.logger.info("loading users...")
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

	def getAllUsers(self):
		""" Scrapes `/match` page for user profiles """
		url = "http://www.okcupid.com/match"
		if self.driver.current_url != url:
			self.logger.info(url)
			self.driver.get(url)
			time.sleep(5)
			self._cancelLoading()
		self.scrape = False
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
				# submit new user to database
				if self.db.newUser(username, age, location, match, enemy, liked):
					self.scrape = True
			except Exception as e:
				self.takeScreenShot(time.time())
				self.logger.error(e)
				traceback.print_stack()
				time.sleep(360)

	def visitProfile(self, username):
		""" Visits the profile page of a user
			Args:
				username (str): OkCupid username
		"""
		self.logger.info("Visting profile: %s" % username)
		url = "http://www.okcupid.com/profile/%s" % username
		self.driver.get(url)
		time.sleep(5)

	def saveProfile(self, username):
		""" Visits the profile page of a user
			Extracts html and saves it do database
			Args:
				username (str): OkCupid username
		"""
		self.visitProfile(username)
		try:
			self.driver.find_element(By.CSS_SELECTOR, "div.essays2015-expand").click()
		except:
			pass
		time.sleep(0.5)
		source = self.driver.page_source
		self.db.saveProfile(username, source)

