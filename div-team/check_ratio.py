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
div_id  = os.getenv('DIVTEAM_ID')
div_user_id = os.getenv('DIV_USER_ID')
div_user  = os.getenv('DIV_USER')
# Set up logging
logging.basicConfig(filename="../app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://divteam.com/index.php?page=login')

# Load session
with open("div-team-cookies.txt", 'r') as file:
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)


driver.get(f'https://divteam.com/index.php?page=userdetails&id={div_user_id}')
driver.get(f'https://divteam.com/index.php?page=userdetails&id={div_user_id}')

# Find all td elements with the text "Ratio"
elements = driver.find_elements(By.XPATH, "//li[@class='list-group-item bot-flex']/strong[.='Ratio']")

# Ensure there's only one such element
if len(elements) != 1:
    logging.error("Expected one 'Ratio' element, found %s", len(elements))

# Find the li element that contains the ratio
li_element = driver.find_element(By.XPATH, "//li[@class='list-group-item bot-flex' and .//strong[.='Ratio']]")

# Convert the ratio text to an integer
ratio = int(li_element.text.split("Ratio")[1].split('.')[0])

while ratio < 4:
    logging.info("The ratio is less than 4")
    driver.get(f'https://divteam.com/index.php?page=modules&module=seedbonus')
    seedpoints = driver.find_element(By.XPATH, "//section//article[1]//div[1]//h4").text
    seedpoints_remaining = int(seedpoints.split('(')[1].split(')')[0].split(" ")[1].split('.')[0])
    if seedpoints_remaining < 1000:
        logging.error("There are not enough seedpoints to make a purchase.")
        if is_indexer_enabled: disable_indexer(div_id)
        send_email("DivTeam - Seedpoints Error", "DivTeam - There are not enough seedpoints to make a purchase. The indexer has been disabled.")
        exit(1)
    else:
        elements = driver.find_element(By.XPATH, "/html/body/if:is_displayed_3/section/section/section/section/article[1]/table/tbody/tr[4]/td[4]/input").click()
        driver.get(f'https://divteam.com/index.php?page=userdetails&id={div_user_id}')
        li_element = driver.find_element(By.XPATH, "//li[@class='list-group-item bot-flex' and .//strong[.='Ratio']]")
        new_ratio = int(li_element.text.split("Ratio")[1].split('.')[0])
        if new_ratio == ratio:
            logging.error("The ratio has not been updated after the purchase, signalign there are no Bonus Puntos left.")
            if is_indexer_enabled: disable_indexer(div_id)
            send_email("DivTeam - Ratio Error", "DivTeam - No BONs left, prowlarr indexer has been disabled")
            exit(1)
        else:
            if not is_indexer_enabled: enable_indexer(div_id)
            send_email("DivTeam - Upload Purchase", "DivTeam - Ratio was detected to be < 4 and an automated purchase has been made. The indexer has been enabled.")
        ratio = new_ratio
