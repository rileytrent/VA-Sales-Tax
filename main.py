# import requests
# import os
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from dateutil.relativedelta import relativedelta
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
# import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import subprocess

#get current chrome version. 
def get_chrome_ver():
    output = subprocess.check_output(
        ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
    )
    return (output.decode('utf-8').strip().split()[-1])
get_chrome_ver()

# period,tax_id, username_login, password_entry,file_path
def file_tax(period, tax_id, username_login, password_entry, file_path):
    # load_dotenv()

    FILING_NUMBER = tax_id
    USERNAME_LOGIN = username_login
    PASSWORD = password_entry
    FILING_URL = "https://www.business.tax.virginia.gov/VTOL/tax/Login.xhtml"
    # os.getenv("FILING_URL")

# service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version=get_chrome_ver()).install()),options=options)
# webdriver.Chrome(service=service,options=options)

    tax_data = pd.read_csv(file_path)

#Function to get Last Month date in the format to click the correct button for filing - Moved to GUI


    filing_month = period
    # live_target_month_year = get_current_filing_month()

# #Opens Page and dismisses weird warning.
    driver.get(FILING_URL)

    time.sleep(1)

    dismiss_warning = driver.find_element(By.CSS_SELECTOR, '.btn.btn-outline-warning.waves-effect.button-submit')
    dismiss_warning.click()

#Clicks correct log in format.
    Tax_button = driver.find_element(By.CSS_SELECTOR, 'input[name="loginForm:customerType"][value="T"]')
    Tax_button.click()

#Fills out Login Info
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


#Selects correct tax filing, Sales and Use Tax
    file_and_pay_button = driver.find_element(By.LINK_TEXT, "File / Pay Use Tax")
    file_and_pay_button.click()

    time.sleep(1)

#nice Try Iframe
    iframe = driver.switch_to.frame("tapsIFrame")

    time.sleep(1)

#Calls Function to get correct Filing month, the previous month, and clicks it to open it.
    test_case = (f"//td[normalize-space()='{filing_month}']/parent::tr//a[contains(text(),'File Now')]")

    current_month_button = driver.find_element(By.XPATH, test_case)
    current_month_button.click()


    time.sleep(1)

#filling out form details. Javascript is an evil little man. Nonclickable buttons. 
    driver.execute_script("selectAll();")

    time.sleep(1)

    driver.execute_script("onClickCreateReturn(document.querySelector('a.btn.btn-secondary'));")

    time.sleep(1)

#expands all to recieve numbies. 
    driver.execute_script("expandAll();")

    time.sleep(1)

#Add function to fill out the boxes based on csv file. 

    for _, row in tax_data.iterrows():
        index = int(row['worksheet_index'])  
        value = str(row['gross_general_sales'])

        try:
        # Find input index
            input_selector = f"st1Form:workSheet:{index}:j_idt148:grossSales"
            input_elem = driver.find_element(By.NAME, input_selector)
            input_elem.clear()
            input_elem.send_keys(value)
        except Exception as e:
            print(f"Failed for row {index}: {e}")

    time.sleep(1)
#click calculate button
    calculate_button = driver.find_element(By.NAME, 'st1Form:j_idt213')
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView(true);", calculate_button)
    time.sleep(1)
    calculate_button.click()

    time.sleep(1)
#click button for review
    for_review_button = driver.find_element(By.NAME, 'st1Form:j_idt111')
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView(true);", for_review_button)
    time.sleep(1)
    for_review_button.click()

