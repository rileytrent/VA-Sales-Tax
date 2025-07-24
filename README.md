# VA-Sales-Tax

Files VA Sales Tax - Only Works on Google Chrome

Simple way to file sales tax for remote sellers in Virginia.

Virginia Requires all sales tax filings to be done on a local level.

Set-up:
This program requies you set up a .env file with the correct filing information and a .csv Filing template named "data.csv" . Examples Below.
You should use the provided Template.csv

.env

```
VA_SALES_TAX_NUMBER = "Your_TIN_or_EIN"

VA_SALES_TAX_LOGIN = "Your_Username"

VA_SALES_TAX_PW = "Your_password"

FILING_URL = "VA_Remote_sales_tax_login_page"
```

data.csv

```
locality_code,county_name,gross_general_sales,worksheet_index
51001,Accomack,10,0
51003,Albemarle,10,1
51510,Alexandria,10,2
51005,Alleghany,10,3
...
51195,Wise,10,131
51197,Wythe,10,132
51199,York,10,133
```
