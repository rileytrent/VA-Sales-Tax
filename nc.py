import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
nc_test_template = "NC_TAX_TEMPLATE.csv"



#get current chrome version. 
def set_value_js_by_name(driver, name, value_str):
    elem = driver.find_element(By.NAME, name)
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].defaultValue = arguments[1];  // so their code treats it as the original
    """, elem, value_str)

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

    tax_data = pd.read_csv(file_path)
    print(tax_data)

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

    time.sleep(1)
    #Summary main page loop
    for _, row in tax_data.iterrows():
        county_juris = str(row['county_juris']) 
        state_tax = float(row['state_tax']) 
        high_local_tax = float(row['high_local_tax'])
        low_local_tax = float(row['low_local_tax'])
        transit_tax = float(row['transit_tax'])
        gross_sales = float(row['gross_sales'])

        try:
        # Find input index
            if county_juris == 'GROSS TOTAL':
                set_value_js_by_name(driver, 'gross-receipts', f"{gross_sales:.2f}")
            elif county_juris == 'SUBTOTAL':
                set_value_js_by_name(driver, 'receipts-state-0475', f"{state_tax:.2f}")
                set_value_js_by_name(driver, 'receipts-county-020', f'{low_local_tax}')
                set_value_js_by_name(driver, 'receipts-county-0225',f'{high_local_tax}')
                set_value_js_by_name(driver, 'receipts-county-005', f'{transit_tax}')
            else:
                pass
        except Exception as e:
            print(f"Failed for row {county_juris}: {e}")
    
    time.sleep(1)

    next_button = driver.find_element(By.NAME, 'img_next')
    next_button.click()

    time.sleep(1)

    next_button = driver.find_element(By.NAME, 'img_next')
    next_button.click()

    time.sleep(1)

    for _, row in tax_data.iterrows():
        county_juris = str(row['county_juris']) 
        state_tax = float(row['state_tax']) 
        high_local_tax = float(row['high_local_tax'])
        low_local_tax = float(row['low_local_tax'])
        transit_tax = float(row['transit_tax'])
        high_local_box = str(row['county_2_25pct_input'])
        low_local_box = str(row['county_2pct_input'])
        transit_box = str(row['transit_0_5pct_input'])
        gross_sales = float(row['gross_sales'])

        try:
        # Find input index
            if county_juris == 'GROSS TOTAL' or county_juris == 'NON TAXABLE TOTAL' or county_juris == 'GROSS TOTAL' :
                pass
            elif high_local_tax != 0 and low_local_tax == 0 and transit_tax == 0:
                set_value_js_by_name(driver, high_local_box, f"{high_local_tax:.2f}")
            elif high_local_tax != 0 and low_local_tax == 0 and transit_tax != 0:
                set_value_js_by_name(driver, high_local_box, f"{high_local_tax:.2f}")
                set_value_js_by_name(driver, transit_box, f"{transit_tax:.2f}")
            elif high_local_tax == 0 and low_local_tax != 0 and transit_tax == 0:
                set_value_js_by_name(driver, low_local_box, f"{low_local_tax:.2f}")
            elif high_local_tax == 0 and low_local_tax != 0 and transit_tax != 0:
                set_value_js_by_name(driver, low_local_box, f"{low_local_tax:.2f}")
                set_value_js_by_name(driver, transit_box, f"{transit_tax:.2f}")
            else:
                pass
        except Exception as e:
            print(f"Failed for row {county_juris}: {e}")

    time.sleep(1)

    driver.execute_script("""
    // Recalculate all totals based on the current field values
    totalTwoPercent();
    totalTwoFiveFivePercent();
    totalPointFivePercent();
    """)
    time.sleep(1)
    summary_button = driver.find_element(By.NAME, 'img_e500')
    summary_button.click()

#local testing 
NC_file_tax(nc_test_login_name, nc_test_email, nc_test_phone, nc_test_account_id, nc_test_period, nc_test_ein, nc_test_template)
