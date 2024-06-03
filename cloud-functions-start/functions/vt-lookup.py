import requests
import os
import json
import datetime
import time

api_key = os.environ.get("VT_API")
url = "https://www.virustotal.com/api/v3/urls"

payload = { "url": "www.facebook.com" }
headers = {
    "accept": "application/json",
    "x-apikey": api_key,
    "content-type": "application/x-www-form-urlencoded"
}

# first we have to go and get the request for the url 
response = requests.post(url, data=payload, headers=headers)
response_json = json.loads(response.text)

# from the response we can get the link to the actual scan
scan_response = requests.get(response_json['data']['links']['self'], headers=headers)
scan_response_json = json.loads(scan_response.text)
dt = datetime.datetime.fromtimestamp(scan_response_json['data']['attributes']['date']).strftime("%d/%m/%Y %H:%M:%S")
while scan_response_json['data']['attributes']['status'] != 'completed':
    print(f"Scan status : {scan_response_json['data']['attributes']['status']}")
    time.sleep(30)
    scan_response = requests.get(response_json['data']['links']['self'], headers=headers)
    scan_response_json = json.loads(scan_response.text)
    
scan_results = scan_response_json['data']['attributes']['stats']
print(scan_response_json['data']['attributes']['status'])
print(f"{dt}: {scan_results}")

def decision_engine(scan_results):
    total = scan_results['malicious'] + scan_results['suspicious'] + scan_results['harmless']
    bad = scan_results['malicious'] + scan_results['suspicious']
    harmless = scan_results['harmless']
    percentage = round(harmless / total * 100)

    if percentage >= 5:
        print(f"PASSED : {percentage}% confirmed ok")
    else:
        print(f"FAILED threshold! : {bad} engines report suspicious or malicious. Out of {total}. Refer for manual checking")

decision_engine(scan_results)
