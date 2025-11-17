import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import calendar
import pandas as pd
import subprocess
import os 
from dotenv import load_dotenv




#Local Dev testing
load_dotenv()
nc_test_email = os.getenv("NC_SALES_TAX_CONTACT_EMAIL") #this number wont change in prod so no need to collect it in the gui
nc_test_login_name = os.getenv("NC_SALES_TAX_CONTACT_NAME") #this number wont change in prod so no need to collect it in the gui
nc_test_phone = os.getenv("NC_SALES_TAX_CONTACT_PHONE") #this number wont change in prod so no need to collect it in the gui
nc_test_filing_url = os.getenv("NC_SALES_TAX_FILING_URL") #this number wont change in prod so no need to collect it in the gui
nc_test_account_id = os.getenv("NC_SALES_TAX_ACCOUNT_ID") #this number wont change in prod so no need to collect it in the gui
nc_test_ein = os.getenv("BARKINGLABS_EIN")
nc_test_period = "Oct 2025"



#get current chrome version. 
def get_chrome_ver():
    output = subprocess.check_output(
        ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
    )
    return (output.decode('utf-8').strip().split()[-1])
get_chrome_ver()

def get_filing_date(date):
    dt = datetime.strptime(date, "%b %Y")
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    result = f"{dt.month:02d}-{last_day:02d}-{dt.year}"
    return result

# period,tax_id, username_login, password_entry,file_path
def NC_file_tax(contact_name, contact_email, contact_phone, account_id, period, ein, file_path):
    CONTACT_NAME = contact_name
    CONTACT_EMAIL = contact_email
    CONTACT_PHONE = contact_phone
    ACCOUNT_ID = account_id
    PERIOD = get_filing_date(period)
    PERIOD_INFO = PERIOD.split("-")
    MONTH = PERIOD_INFO[0]
    DAY = PERIOD_INFO[1]
    YEAR= PERIOD_INFO[2]
    EIN = ein
    FILING_URL = "https://eservices.dor.nc.gov/sau/contact.jsp"

    # os.getenv("FILING_URL")

# service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version=get_chrome_ver()).install()),options=options)

    driver.get(FILING_URL)

    time.sleep(1)
    #Fills out Login Info
    name = driver.find_element(By.NAME, 'name')
    name.send_keys(CONTACT_NAME)

    email = driver.find_element(By.NAME, 'email')
    email.send_keys(CONTACT_EMAIL)

    phone_number = driver.find_element(By.NAME, 'phone')
    phone_number.send_keys(CONTACT_PHONE)

    time.sleep(1)

    next_button = driver.find_element(By.NAME, 'img_next')
    next_button.click()

    time.sleep(1)

    id = driver.find_element(By.NAME, 'salesacctnumber')
    id.send_keys(ACCOUNT_ID)
    
    time.sleep(1)

    submit_button = driver.find_element(By.NAME, 'img_submit')
    submit_button.click()

    time.sleep(1)

    next_button = driver.find_element(By.NAME, 'img_next')
    next_button.click()

    time.sleep(1)

    file_type_selector = driver.find_element(By.CSS_SELECTOR, "input[name='filingOption'][value='filePay']")
    file_type_selector.click()

    time.sleep(1)

    next_button = driver.find_element(By.NAME, 'img_next')
    next_button.click()

    time.sleep(1)

    month_selector = Select(driver.find_element(By.NAME, 'periodEndMonth'))
    month_selector.select_by_value(f"{MONTH}")

    time.sleep(1)

    day_selector = Select(driver.find_element(By.NAME, 'periodEndDay'))
    day_selector.select_by_value(f"{DAY}")

    time.sleep(1)

    year_selector = Select(driver.find_element(By.NAME, 'periodEndYear'))
    year_selector.select_by_value(f"{YEAR}")

    time.sleep(1)

    fein_type_selector = driver.find_element(By.CSS_SELECTOR, "input[name='entityType'][value='001']")
    fein_type_selector.click()

    time.sleep(1)

    id = driver.find_element(By.NAME, 'entityIDFID1')
    id.send_keys(EIN[:2])

    id = driver.find_element(By.NAME, 'entityIDFID2')
    id.send_keys(EIN[-7:])

    time.sleep(1)

    next_button = driver.find_element(By.NAME, 'img_next')
    next_button.click()
    
#local testing 
NC_file_tax(nc_test_login_name, nc_test_email, nc_test_phone, nc_test_account_id, nc_test_period, nc_test_ein, None)
