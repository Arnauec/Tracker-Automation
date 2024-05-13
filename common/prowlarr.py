import json
import logging
import requests
from dotenv import load_dotenv
import os
from time import sleep
from common.email_utils import send_email


# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the .env file
load_dotenv()

# Now you can access the variables
prowlarr_ip  = os.getenv('PROWLARR_IP')
prowlarr_api = os.getenv('PROWLARR_API_KEY')
# Define the Prowlarr API URL
prowlarr_url = f'http://{prowlarr_ip}:9696/api/v1'

def is_indexer_enabled(indexer_id):
    # Get the current configuration of the indexer
    response = requests.get(f'{prowlarr_url}/indexer/{indexer_id}', params={'apikey': prowlarr_api})
    indexer_config = response.json()

    # Check if the indexer is enabled
    if indexer_config['enable']:
        return True
    else:
        return False

def disable_indexer(indexer_id):
    # Get the current configuration of the indexer
    response = requests.get(f'{prowlarr_url}/indexer/{indexer_id}', params={'apikey': prowlarr_api})
    indexer_config = response.json()

    # Set the 'enable' field to False to disable the indexer
    indexer_config['enable'] = False

    # Update the indexer configuration
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f'{prowlarr_url}/indexer/{indexer_id}', params={'apikey': prowlarr_api}, data=json.dumps(indexer_config), headers=headers)

    # Check if the request was successful
    if response.status_code == 202:
        logging.info(f'Indexer disabled successfully. Indexer ID: {indexer_id}')
    else:
        logging.error(f'Failed to disable indexer. Indexer ID: {indexer_id}')

def enable_indexer(indexer_id):
    # Get the current configuration of the indexer
    response = requests.get(f'{prowlarr_url}/indexer/{indexer_id}', params={'apikey': prowlarr_api})
    indexer_config = response.json()

    # Set the 'enable' field to True to enable the indexer
    indexer_config['enable'] = True

    # Update the indexer configuration
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f'{prowlarr_url}/indexer/{indexer_id}', params={'apikey': prowlarr_api}, data=json.dumps(indexer_config), headers=headers)

    # Check if the request was successful
    if response.status_code == 202:
        logging.info(f'Indexer enabled successfully. Indexer ID: {indexer_id}')
    else:
        logging.error(f'Failed to enable indexer. Indexer ID: {indexer_id}')