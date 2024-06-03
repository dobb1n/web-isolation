import requests
import os
import json

api_key = os.environ.get("VT_API")
url = "https://www.virustotal.com/api/v3/urls"

payload = { "url": "www.test.com" }
headers = {
    "accept": "application/json",
    "x-apikey": api_key,
    "content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == 200:
    vt_url_scan = json.loads(response.text)
    site_q_url = f"{vt_url_scan['data']['links']['self']}"
    scan_response = requests.get(site_q_url, headers=headers)
    if scan_response.status_code == 200:
        site_stats = json.loads(scan_response.text)
        print(site_stats['data']['attributes']['stats'])
    else:
        print(f"Couldnt get site report : {scan_response.status_code}")
else:
    print(f"didnt get an answer {response.status_code}")
