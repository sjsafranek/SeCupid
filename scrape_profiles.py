#!/usr/bin/python

import argparse
import SeCupid

def scrape(usr, psw):
	cupid = SeCupid.SeCupid(usr, psw, headless=True)
	cupid.login()
	for user in cupid.db.getUsers():
		print("Scraping profile: %s" % user.username)
		cupid.saveProfile(user.username)
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
	args = parser.parse_args()
	scrape(args.u, args.p)