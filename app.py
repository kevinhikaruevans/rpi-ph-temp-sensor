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

def perform_api_request(sensor, value, timestamp=None):
    try:
        requests.post(f"{API_HOST}/api/entries/push", timeout=API_TIMEOUT, json={
            "token": API_TOKEN,
            "sensor": sensor,
            "value": value
        })
    except Exception as e:
        print('failed to post request', e)

def perform_dry_run():
    print("Performing dry run...")
    print("tempC: ", read_temp())
    print("   pH: ", read_ph())
    print("--------------------------")


if __name__ == "__main__":
    while True:
        if args.dry_run:
            perform_dry_run()
        else:
            timestamp = int(time.time())
            temp = read_temp()
            pH = read_ph()

            perform_api_request("Temperature", temp, timestamp)
            perform_api_request("pH", pH, timestamp)

        time.sleep(POLL_DELAY)