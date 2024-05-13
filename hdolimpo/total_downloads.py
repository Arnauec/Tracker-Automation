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
from datetime import datetime, timedelta
import transmission_rpc

# Set up logging
logging.basicConfig(filename="../app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the .env file
load_dotenv()

# Now you can access the variables
trans_ip = os.getenv('TRANS_IP')
username = os.getenv('TRANS_USER')
password = os.getenv('TRANS_PW')

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


driver.get('https://hd-olimpo.club/users/arnauec')

# Calculate the date 90 days ago
date_90_days_ago = datetime.now() - timedelta(days=90)


# Navigate to the page with the table
driver.get('https://hd-olimpo.club/users/arnauec/torrents?downloaded=include&perPage=1000')


# Find all rows
rows = driver.find_elements(By.XPATH, "//tr[td[@class='user-torrents__completed-at']]")

# Filter rows where the "user-torrents__completed-at" column is later than 90 days ago
recent_rows = [row for row in rows if datetime.strptime(row.find_element(By.XPATH, "td[@class='user-torrents__completed-at']").text, '%Y-%m-%d') > date_90_days_ago]

# Check if the total number of rows is less than 14
if len(rows) > 14:
    logging.info("More than 14 torrents downloaded during the last 90 days")
    pass
else:
    for i in range(14-len(rows)):
        driver.get('https://hd-olimpo.club/torrents?perPage=50&free[0]=100&page='+str(random.randint(1, 60)))
        elements = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/section/article/div/div/section/div[2]/table/tbody/tr[1]/td[3]/a").click()
        # Find the a element that contains the text "Descargar"
        torrent_url = driver.find_element(By.XPATH, "//a[contains(text(), 'Descargar')]").get_attribute('href')
        logging.info("Downloading a new torrent to satisfy 10 torrents every 90 days requirement. Torrent URL: " + torrent_url)
        # Get cookies from Selenium
        cookies = driver.get_cookies()

        # Create a new requests session
        s = requests.Session()

        # Add the cookies to the session
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])

        # Now you can use the session to make requests with the same cookies as the Selenium session
        response = s.get(torrent_url)
        torrent_id = torrent_url.split('/')[-1]
        # Save the torrent file to a temporary file
        with open(f'./torrents/{torrent_id}.torrent', 'wb') as f:
            f.write(response.content)

        # Connect to the Transmission RPC server
        client = transmission_rpc.Client(host=trans_ip, port=9091, username=username, password=password)

        # Read the torrent file content
        with open(f'./torrents/{torrent_id}.torrent', 'rb') as f:
            torrent_data = f.read()

        # Add a torrent
        torrent = client.add_torrent(torrent_data)

        # Start the torrent
        client.start_torrent(torrent.id)