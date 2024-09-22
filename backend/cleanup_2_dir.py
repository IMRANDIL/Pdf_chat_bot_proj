import requests
import time
import logging
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Load environment variables
import os
base_uri = os.getenv('BASE_URI')
# URL of the cleanup route
CLEANUP_URL = f"{base_uri}/clean-upload-folder"

def schedule_cleanup():
    while True:
        try:
            # Make a GET request to the clean-upload-folder API
            response = requests.get(CLEANUP_URL)
            
            # Log the response
            if response.status_code == 200:
                logging.info("Cleanup successful: %s", response.json()['message'])
            else:
                logging.error("Cleanup failed: %s", response.json().get('error', 'Unknown error'))
        
        except Exception as e:
            logging.error("Error during cleanup: %s", str(e))
        
        # Wait for 5 minutes before the next cleanup
        time.sleep(3600)  # 300 seconds = 5 minutes
