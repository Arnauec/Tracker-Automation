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
username = os.getenv('LAT_USER')
password = os.getenv('LAT_PW')

# Set up Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Set up WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get('https://lat-team.com/login')

# Find the username and password fields and enter text
username_field = driver.find_element(By.NAME, 'username')  
password_field = driver.find_element(By.NAME, 'password') 
username_field.send_keys(username)  
password_field.send_keys(password)  

# Find the submit button and click it
submit_button = driver.find_element(By.XPATH, "/html/body/main/section/form/div[2]/button") 
submit_button.click()

# Confirm login was successful
driver.get(f'https://lat-team.com/users/{username}') # Replace with your user ID
user_name = driver.find_element(By.XPATH, '//*[@title="User"]').text

# Check if the text contains the desired words
if "arnauec" in user_name:
    logging.info(f"The text '{username}' is present in the userMenu element. Login Successful!")
else:
    logging.error(f"The text '{username}' is not present in the userMenu element. There was a problem during Login.")
    send_email("LAT-Team - Login Error", f"LAT-Team - There was an error during logging. The text '{username}' was not present in the userMenu element.")

cookies = driver.get_cookies()
with open("lat-team-cookies.txt", 'w') as file:
    json.dump(cookies, file)