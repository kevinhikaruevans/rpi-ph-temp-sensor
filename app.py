from dotenv import load_dotenv
import time
import argparse
import requests
import os
from sensors import read_temp, read_ph

load_dotenv()

API_HOST = os.getenv('API_HOST')
API_TOKEN = os.getenv('API_TOKEN')
API_TIMEOUT = 10 # seconds
POLL_DELAY = 60 # seconds

parser = argparse.ArgumentParser(description='Read sensor data and send to API')
parser.add_argument('--dry-run', action='store_true', help='Do not send data to API')
args = parser.parse_args()

def perform_api_request():
    r = requests.post(f"https://{API_TOKEN}/api/sensors", timeout=API_TIMEOUT, json={
        "temperature": read_temp(),
        "ph": read_ph()
    })

def perform_dry_run():
    print("Performing dry run...")
    print("tempC: ", read_temp())
    print("   pH: ", read_ph())
    print("--------------------------")


while True:
    if args.dry_run:
        perform_dry_run()
    else:
        perform_api_request()

    time.sleep(POLL_DELAY)