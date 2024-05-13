import json
import random
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
hdolimpo_id  = os.getenv('HDOLIMPO_ID')
hdolimpo_user = os.getenv('HDOLIMPO_USER')

# Set up logging
logging.basicConfig(filename="../app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://hd-olimpo.club/login')

# Load session
with open("hdolimpo-cookies.txt", 'r') as file:
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)


driver.get('https://hd-olimpo.club/users/{hdolimpo_user}')
driver.get('https://hd-olimpo.club/users/{hdolimpo_user}')
sleep(2)
# Find all td elements with the text "Ratio"
elements = driver.find_elements(By.XPATH, "//td[.='Ratio']")

# Ensure there's only one such element
if len(elements) != 1:
    logging.error("Expected one 'Ratio' element, found %s", len(elements))

# Find the next td element
ratio = int(driver.find_element(By.XPATH, "//td[.='Ratio']/following-sibling::td").text.split('.')[0])
agradecimientos = int(driver.find_element(By.XPATH, "//td[.='Ratio agradecimiento']/following-sibling::td").text.split('.')[0])

while ratio < 4:
    logging.info("The ratio is less than 4")
    driver.get('https://hd-olimpo.club/bonus/store')
    elements = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/section/article/div/div/div[3]/div/div[1]/div/table/tbody/tr[5]/td[3]/form/button").click()
    driver.get('https://hd-olimpo.club/users/{hdolimpo_user}')
    new_ratio = int(driver.find_element(By.XPATH, "//td[.='Ratio']/following-sibling::td").text.split('.')[0])
    if new_ratio == ratio:
        logging.error("The ratio has not been updated after the purchase, signalign there are no BONs left.")
        if is_indexer_enabled: disable_indexer(hdolimpo_id)
        send_email("HDOlimpo - Ratio Error", "HDOlimpo - No BONs left, prowlarr indexer has been disabled")
        exit(1)
    else:
        send_email("HDOlimpo - Upload Purchase", "HDOlimpo - Ratio was detected to be < 4 and an automated purchase has been made.")
        if not is_indexer_enabled: enable_indexer(hdolimpo_id)
    ratio = new_ratio

while agradecimientos < 2:
    logging.info("Agradecimientos is less than 2")
    driver.get('https://hd-olimpo.club/torrents?perPage=25&sortField=created_at&sortDirection=asc&page='+str(random.randint(1, 1500)))
    elements = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/section/article/div/div/section/div[2]/table/tbody/tr[1]/td[3]/a").click()
    button = driver.find_element(By.XPATH, "//button[contains(., 'Agradecer')]").click()
    driver.get(f'https://hd-olimpo.club/users/{hdolimpo_user}')
    agradecimientos = int(driver.find_element(By.XPATH, "//td[.='Ratio agradecimiento']/following-sibling::td").text.split('.')[0])
    send_email("HDOlimpo - Agradecimiento done", "HDOlimpo - Agradecimiento ratio was detected to be < 4 and an automated agradecimiento has been made.")