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


load_dotenv()

FILING_NUMBER = os.getenv("VA_SALES_TAX_NUMBER")
USERNAME_LOGIN = os.getenv("VA_SALES_TAX_LOGIN")
PASSWORD = os.getenv("VA_SALES_TAX_PW")
FILING_URL = os.getenv("FILING_URL")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#Opens Page and dismisses weird warning.
driver.get(FILING_URL)

time.sleep(2)

dismiss_warning = driver.find_element(By.CSS_SELECTOR, '.btn.btn-outline-warning.waves-effect.button-submit')
dismiss_warning.click()






#Log Into VA sales Tax 

