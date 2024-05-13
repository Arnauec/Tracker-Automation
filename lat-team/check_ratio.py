import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import logging
from time import sleep
from common.email_utils import send_email
from common.prowlarr import disable_indexer, enable_indexer, is_indexer_enabled

# Load the .env file
load_dotenv()

# Now you can access the variables
latteam_id  = os.getenv('LATTEAM_ID')
latteam_user  = os.getenv('LAT_USER')
# Set up logging
logging.basicConfig(filename="../app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://lat-team.com/login')

# Load session
with open("lat-team-cookies.txt", 'r') as file:
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)


driver.get(f'https://lat-team.com/users/{latteam_user}')
driver.get(f'https://lat-team.com/users/{latteam_user}')

# Find all td elements with the text "Ratio"
elements = driver.find_elements(By.XPATH, "//dt[.='Proporción']")

# Ensure there's only one such element
if len(elements) != 1:
    logging.error("Expected one 'Ratio' element, found %s", len(elements))

# Find the next td element
ratio = int(driver.find_element(By.XPATH, "//dt[.='Proporción']/following-sibling::dd").text.split('.')[0])

while ratio < 4:
    logging.info("The ratio is less than 4")
    driver.get(f'https://lat-team.com/users/{latteam_user}/transactions/create')
    elements = driver.find_element(By.XPATH, "/html/body/main/article/div/section/div/table/tbody/tr[4]/td[3]/form/button").click()
    driver.get(f'https://lat-team.com/users/{latteam_user}')
    new_ratio = int(driver.find_element(By.XPATH, "//dt[.='Proporción']/following-sibling::dd").text.split('.')[0])
    if new_ratio == ratio:
        logging.error("The ratio has not been updated after the purchase, signalign there are no Bonus Puntos left.")
        if is_indexer_enabled: disable_indexer(latteam_id)
        send_email("HDOlimpo - Ratio Error", "HDOlimpo - No BONs left, prowlarr indexer has been disabled")
        exit(1)
    else:
        if not is_indexer_enabled: enable_indexer(latteam_id)
        send_email("HDOlimpo - Upload Purchase", "HDOlimpo - Ratio was detected to be < 4 and an automated purchase has been made. The indexer has been enabled.")
    ratio = new_ratio
