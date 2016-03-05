#!/usr/bin/python

# OkCupid_Se

__author__ = "Stefan Safranek"
__copyright__ = "Copyright 2016, SeCupid"
__credits__ = ["Stefan Safranek"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Stefan Safranek"
__email__ = "https://github.com/sjsafranek"
__status__ = "Development"

import os
import time
import builtins
import traceback
import Conf
import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains


class SeCupid(object):
	""" Selenium Handler for OkCupid """

	def __init__(self, username, password, headless=False):
		""" Initiate SeCupid Class
			Args:
				username (str): OkCupid username
				password (str): OkCupid password
		"""
		# setup database
		self.db = Database.DB()
		# Setup browser
		self.username = username
		self.password = password
		if headless:
			self.driver = webdriver.PhantomJS("phantomjs-2.0.0-linux/phantomjs")
		else:
			self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(10)
		# options
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
		# CHECK FOR FAILURE
		if "Your info was incorrect. Try again." in self.driver.find_element(By.TAG_NAME, "body").text:
			self.driver.quit()
			raise ValueError("Your info was incorrect. Try again.")
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

	def getAllUsers(self):
		""" Scrapes `/match` page for user profiles """
		url = "http://www.okcupid.com/match"
		if self.driver.current_url != url:
			print(url)
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

	def saveProfile(self, username):
		""" Visits the profile page of a user
			Extracts html and saves it do database
			Args:
				username (str): OkCupid username
		"""
		self.visitProfile(username)
		source = self.driver.page_source
		self.db.saveProfile(username, source)

	def setFilters(self, **kwargs):
		""" Scrapes `/match` page for user profiles """
		print(kwargs)
		url = "http://www.okcupid.com/match"
		if self.driver.current_url != url:
			print(url)
			self.driver.get(url)
			time.sleep(5)
			self._cancelLoading()
		# Age range - high
		if "age_max" in kwargs:
			container = self.driver.find_element(By.CSS_SELECTOR, "span.filter-wrapper.filter-age")
			container.find_element(By.TAG_NAME, "button").click()
			self.driver.find_element(By.NAME, "maximum_age").send_keys(
				Keys.BACKSPACE*3 + str(kwargs["age_max"]) + Keys.RETURN)
		# Age range - low
		if "age_min" in kwargs:
			container = self.driver.find_element(By.CSS_SELECTOR, "span.filter-wrapper.filter-age")
			container.find_element(By.TAG_NAME, "button").click()
			self.driver.find_element(By.NAME, "minimum_age").send_keys(
				Keys.BACKSPACE*3 + str(kwargs["age_min"]) + Keys.RETURN)
		# Men
		if "men" in kwargs:
			### STILL WORKING ON CHECKBOX HANDLING
			container = self.driver.find_element(By.CSS_SELECTOR, "span.filter-wrapper.filter-gender")
			container.find_element(By.TAG_NAME, "button").click()
			for item in se.driver.find_elements(By.CSS_SELECTOR, "label.checkbox-wrapper"):
				if "Men" in item.text and kwargs['men']:
					item.find_element(By.CSS_SELECTOR, "div.decoration").click()
					break
			container = se.driver.find_element(By.CSS_SELECTOR, "span.filter-wrapper.filter-gender")
		# Women
		if "women" in kwargs:
			### STILL WORKING ON CHECKBOX HANDLING
			container = self.driver.find_element(By.CSS_SELECTOR, "span.filter-wrapper.filter-gender")
			container.find_element(By.TAG_NAME, "button").click()
			for item in se.driver.find_elements(By.CSS_SELECTOR, "label.checkbox-wrapper"):
				if "Women" in item.text and kwargs['women']:
					item.find_element(By.CSS_SELECTOR, "div.decoration").click()
					break
			container.find_element(By.TAG_NAME, "button").click()
		# Open filters section
		self.driver.find_element(By.CSS_SELECTOR, "button.toggle-advanced-filters.toggle-advanced-filters--collapsed").click()
		# Single or Not
		if "single" in kwargs:
			self.driver.find_element(By.CSS_SELECTOR, "button.advanced-filter-toggle.advanced-filter-toggle-availability").click()
			container = self.driver.find_element(By.CSS_SELECTOR, "div.filter.toggle-and-clear.value-set.filter-availability")
			for button in container.find_elements(By.TAG_NAME, "button"):
				if kwargs["single"] and button.text == "Single":
					if "selected" not in button.get_attribute("class"):
						button.click()
						break
				if not kwargs["single"] and button.text == "Not single":
					if "selected" not in button.get_attribute("class"):
						button.click()
						break
		# Monogomus
		if "monogamous" in kwargs:
			self.driver.find_element(By.CSS_SELECTOR, "button.advanced-filter-toggle.advanced-filter-toggle-availability").click()
			container = self.driver.find_element(By.CSS_SELECTOR, "div.filter.toggle-and-clear.value-set.filter-monogamy")
			for button in container.find_elements(By.TAG_NAME, "button"):
				if kwargs["monogamous"] and button.text == "Yes":
					if "selected" not in button.get_attribute("class"):
						button.click()
						break
				if not kwargs["monogamous"] and button.text == "No":
					if "selected" not in button.get_attribute("class"):
						button.click()
						break
		# Submit
		for button in self.driver.find_elements(By.CSS_SELECTOR, "button.flatbutton.big.green"):
			if button.text == "Search":
				button.click()
				break

