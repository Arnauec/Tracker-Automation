import json
import random
import requests
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
myanona_id  = os.getenv('MYANONA_ID')
myanona_user_id  = os.getenv('MYANONA_USER_ID')
# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://www.myanonamouse.net/login.php')

# Load session
with open("myanona-cookies.txt", 'r') as file:
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)


driver.get(f'https://www.myanonamouse.net/u/')
driver.get(f'https://www.myanonamouse.net/u/')

# Find all td elements with the text "Ratio"
elements = driver.find_elements(By.XPATH, "//td[.='Share ratio']")

# Ensure there's only one such element
if len(elements) != 1:
    logging.error("Expected one 'Share ratio' element, found %s", len(elements))

# Find the next td element
ratio = int(driver.find_element(By.XPATH, "//td[.='Share ratio']/following-sibling::td").text.split('.')[0].replace(",", ""))

while ratio < 2000:
    logging.info("The ratio is less than 4")
    driver.get(f'https://www.myanonamouse.net/store.php')
    bonus_points_text = driver.find_element(By.XPATH, "//section//article[1]//div[1]//h4").text
    bonus_points = int(bonus_points_text.split('(')[1].split(')')[0].split(" ")[1].split('.')[0])
    if bonus_points < 500:
            logging.error("There are not enough bonus points to make a purchase.")
            if is_indexer_enabled: disable_indexer(myanona_id)
            send_email("MyAnonaMouse - Bonus Points Error", "MyAnonaMouse - There are not enough bonus points to make a purchase. The indexer has been disabled.")
            exit(1)
    else:
        purchase = driver.find_element(By.XPATH, '//button[@title="500 points"]').click()
        confirm =  driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/button[1]').click()
        driver.get(f'https://www.myanonamouse.net/u/')
        new_ratio = int(driver.find_element(By.XPATH, "//td[.='Share ratio']/following-sibling::td").text.split('.')[0].replace(",", ""))
        if new_ratio == ratio:
            logging.error("The ratio has not been updated after the purchase, signalign there are no Bonus Puntos left.")
            if is_indexer_enabled: disable_indexer(myanona_id)
            send_email("MyAnonaMouse - Ratio Error", "MyAnonaMouse - No Bonus Points left, prowlarr indexer has been disabled")
            exit(1)
        else:
            if not is_indexer_enabled: enable_indexer(myanona_id)
            send_email("MyAnonaMouse - Upload Purchase", "MyAnonaMouse - Ratio was detected to be < 4 and an automated purchase has been made. The indexer has been enabled.")
        ratio = new_ratio
