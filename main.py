import requests
import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dateutil.relativedelta import relativedelta
import datetime



load_dotenv()

FILING_NUMBER = os.getenv("VA_SALES_TAX_NUMBER")
USERNAME_LOGIN = os.getenv("VA_SALES_TAX_LOGIN")
PASSWORD = os.getenv("VA_SALES_TAX_PW")
FILING_URL = os.getenv("FILING_URL")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def get_current_filing_month():
    last_month = datetime.datetime.now() - relativedelta(months=1)
    text = last_month.strftime('%B %Y')
    return (text)

target_month_year = get_current_filing_month()
# print(target_month_year)
# print(f"//td[normalize-space()='{target_month_year}']/parent::tr//a[contains(text(),'File Now')]")
# #Opens Page and dismisses weird warning.
driver.get(FILING_URL)

time.sleep(2)

dismiss_warning = driver.find_element(By.CSS_SELECTOR, '.btn.btn-outline-warning.waves-effect.button-submit')
dismiss_warning.click()

Tax_button = driver.find_element(By.CSS_SELECTOR, 'input[name="loginForm:customerType"][value="T"]')
Tax_button.click()

account_number = driver.find_element(By.ID, 'loginForm:customerNumber')
account_number.send_keys(FILING_NUMBER)

login = driver.find_element(By.ID, 'loginForm:userName')
login.send_keys(USERNAME_LOGIN)

password = driver.find_element(By.ID, 'loginForm:password')
password.send_keys(PASSWORD)

time.sleep(1)

login_button = driver.find_element(By.NAME, 'loginForm:loginButton')
login_button.click()

time.sleep(1)

file_and_pay_button = driver.find_element(By.LINK_TEXT, "File / Pay Use Tax")
file_and_pay_button.click()

time.sleep(1)

iframe = driver.switch_to.frame("tapsIFrame")

time.sleep(1)

current_month_button = driver.find_element(By.XPATH, f"//td[normalize-space()='{target_month_year}']/parent::tr//a[contains(text(),'File Now')]")
current_month_button.click()


time.sleep(1)

select_all_button = driver.find_element(By.LINK_TEXT, 'Select All')
login_button.click()

time.sleep(1)

select_all_button = driver.find_element(By.LINK_TEXT, 'Next')
login_button.click()


# <input id="loginForm:loginButton" type="submit" name="loginForm:loginButton" value="Log In" class="button-submit" onclick="return buttonClick(this);" data-di-id="#loginForm:loginButton">

#Log Into VA sales Tax 

# f"//td[text()='{target_month_year}']/parent::tr//a[contains(text(),'File Now')]"