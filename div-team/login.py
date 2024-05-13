import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import logging
from time import sleep
from common.email_utils import send_email
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the .env file
load_dotenv()

# Now you can access the variables
username = os.getenv('DIV_USER')
password = os.getenv('DIV_PW')

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://divteam.com/index.php?page=login')

# Find the username and password fields and enter text
username_field = driver.find_element(By.NAME, 'uid')  
password_field = driver.find_element(By.NAME, 'pwd') 
username_field.send_keys(username)  
password_field.send_keys(password)  

WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
# sleep(15) # In case you need to fill the captcha manually
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
sleep(1)
# Switch back to the main page
driver.switch_to.default_content()

# Find the submit button and click it
submit_button = driver.find_element(By.XPATH, '//input[@value="Confirmar"]')
submit_button.click()

# Confirm login was successful
driver.get('https://divteam.com/') # Replace with your user ID
user_name = driver.find_element(By.CLASS_NAME, 'hidden-xs').text

# Check if the text contains the desired words
if "arnauec" in user_name:
    logging.info("The text 'arnauec' is present in the userMenu element. Login Successful!")
else:
    logging.error("The text 'arnauec' is not present in the userMenu element. There was a problem during Login.")
    send_email("DivTeam - Login Error", "DivTeam - There was an error during logging. The text 'arnauec' was not present in the userMenu element.")

cookies = driver.get_cookies()
with open("div-team-cookies.txt", 'w') as file:
    json.dump(cookies, file)