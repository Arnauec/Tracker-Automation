
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import logging
from time import sleep
from common.email_utils import send_email

# Set up logging
logging.basicConfig(filename="../app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the .env file
load_dotenv()

# Now you can access the variables
username = os.getenv('MYANONA_USER')
password = os.getenv('MYANONA_PW')
myanon_user_id = os.getenv('MYANONA_USER_ID')

# Set up Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://www.myanonamouse.net/login.php')

# Find the username and password fields and enter text
username_field = driver.find_element(By.NAME, 'email')  
password_field = driver.find_element(By.NAME, 'password') 
username_field.send_keys(username)  
password_field.send_keys(password)  

# Find the submit button and click it
submit_button = driver.find_element(By.XPATH, "//input[@value='Log in!']") 
submit_button.click()

# Confirm login was successful
driver.get(f'https://www.myanonamouse.net/u/{myanon_user_id}')
user_name = driver.find_element(By.XPATH, '//*[@id="userMenu"]').text

# Check if the text contains the desired words
if "arnauec" in user_name:
    logging.info("The text 'arnauec' is present in the userMenu element. Login Successful!")
else:
    logging.error("The text 'arnauec' is not present in the userMenu element. There was a problem during Login.")
    send_email("MyAnonaMouse - Login Error", "MyAnonamouse - There was an error during logging. The text 'arnauec' was not present in the userMenu element.")

cookies = driver.get_cookies()
with open("myanona-cookies.txt", 'w') as file:
    json.dump(cookies, file)