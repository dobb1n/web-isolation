import requests
import os
import json
import datetime
import time

api_key = os.environ.get("VT_API")
url = "https://www.virustotal.com/api/v3/urls"

payload = { "url": "www.greatfun.com" }
headers = {
    "accept": "application/json",
    "x-apikey": api_key,
    "content-type": "application/x-www-form-urlencoded"
}

# first we have to go and get the request for the url 
response = requests.post(url, data=payload, headers=headers)
if response.status_code == 200:
    response_json = json.loads(response.text)
else:
    print(f"Went wrong {response.status_code}")
    sys.exit()

# from the response we can get the link to the actual scan
scan_response = requests.get(response_json['data']['links']['self'], headers=headers)
if scan_response.status_code == 200:
    scan_response_json = json.loads(scan_response.text)
else:
    print(f"Something went wrong {scan_response.status_code}")
    sys.exit()

print(scan_response_json)
