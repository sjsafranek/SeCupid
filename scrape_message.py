#!/usr/bin/python

import secupid

import time
import argparse
import traceback
from datetime import datetime
from selenium.webdriver.common.by import By


def run(username, password):
    cupid = secupid.SeCupid(username, password, "chrome")
    cupid.login()

    for user in cupid.db.getUsers():
        try:
            # load user page
            cupid.visitProfile(user.username)

               # open messages
            buttons = cupid.driver.find_elements(By.CSS_SELECTOR, "button.actions2015-chat")
            if 0 != len(buttons):
                buttons[0].click()
                time.sleep(1)
            else: 
                continue

            # loop through messages
            last = -1
            for message in cupid.driver.find_elements(By.CSS_SELECTOR, "div.message"):
                if message.get_attribute("data-timestamp"):
                    try:
                        timestamp = int(message.get_attribute("data-timestamp"))
                        if last < timestamp:
                            last = timestamp
                            user.messaged = True
                    except Exception as e:
                        print(e)
                        traceback.print_stack()

            fmt = "%x %X"
            user.messaged_date = datetime.fromtimestamp(last)
            cupid.logger.info("last messaged: " + user.messaged_date.strftime(fmt))

            # close messages
            messaging_container = cupid.driver.find_element(By.CSS_SELECTOR, "div#global_messaging_container")
            container = messaging_container.find_element(By.CSS_SELECTOR, "div.global_messaging")
            container.find_element(By.CSS_SELECTOR, "i.icon.i-close").click()
            time.sleep(0.5)
            # save to database
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

