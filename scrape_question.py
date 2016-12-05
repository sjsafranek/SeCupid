#!/usr/bin/python

import secupid

import time
import argparse
import traceback
from datetime import datetime
from selenium.webdriver.common.by import By


def getQuestions(driver, user):
    for genreblock in driver.find_elements(By.CSS_SELECTOR, "div.genreblock"):
        label = genreblock.find_element(By.CSS_SELECTOR, "div.genreblock-label").text.lower()
        pct = genreblock.find_element(By.CSS_SELECTOR, "div.genreblock-pct").text.replace("%", "")
        if pct != "--" and pct != "": 
            pct = int(pct)
            if "lifestyle" in label:
                user.lifestyle = pct
            elif "sex" in label:
                user.sex = pct
            elif "dating" in label:
                user.dating = pct
            elif "other" in label:
                user.other = pct
            elif "ethics" in label:
                user.ethics = pct
            elif "religion" in label:
                user.religion = pct


def run(username, password):
    cupid = secupid.SeCupid(username, password, "chrome")
    cupid.login()

    for user in cupid.db.getUsers():
        try:

            cupid.visitProfile(user.username)

            getQuestions(cupid.driver, user)
            cupid.driver.find_element(By.CSS_SELECTOR ,".pageable-pager-btn.pageable-pager-btn--next").click()
            getQuestions(cupid.driver, user)

            user.basics = cupid.driver.find_element(By.CSS_SELECTOR, "table.basics").text
            user.background = cupid.driver.find_element(By.CSS_SELECTOR, "table.background").text
            user.misc = cupid.driver.find_element(By.CSS_SELECTOR, "table.misc").text
            user.looking_for = cupid.driver.find_element(By.CSS_SELECTOR, "div.lookingfor2015-sentence").text

            traits = ""
            for trait in cupid.driver.find_elements(By.CSS_SELECTOR, "div.traits2015-traits-trait"):
                traits += trait.text + ","

            user.traits = traits

            try:
                cupid.db.session.add(user)
                cupid.db.session.commit()
            except Exception as e:
                print(e)
                cupid.db.session.rollback()

        except Exception as e:
            print(e)
            traceback.print_stack()

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
    run(args.u, args.p)
