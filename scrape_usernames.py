#!/usr/bin/python

import secupid
import argparse

def scrape(usr, psw, fast):
	cupid = secupid.SeCupid(usr, psw, "chrome")
	if fast:
		cupid.db.getUsers()
	cupid.login()
	while cupid.scrape:
		cupid.getAllUsers()
	cupid.driver.quit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Selenium OkCupid')
	parser.add_argument('-u', 
						type=str,
						required=True,
						help='okcupid username')
	parser.add_argument('-p', 
						type=str,
					 	required=True,
						help='okcupid password')
	parser.add_argument('-f', 
						# '--fast',
						action="store_true",
					 	required=False,
						help='fast mode')
	args = parser.parse_args()
	scrape(args.u, args.p, args.f)
