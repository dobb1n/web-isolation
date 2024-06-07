import requests
import os
import json
import datetime
import time

from firebase_functions.firestore_fn import (
  on_document_created,
  on_document_deleted,
  on_document_updated,
  on_document_written,
  Event,
  Change,
  DocumentSnapshot,
)
from firebase_functions.params import SecretParam

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore

app = initialize_app()

VIRUSTOTAL_API_KEY = SecretParam('VIRUSTOTAL_API_KEY')

@on_document_created(document="messages/{docID}", region="europe-west2", secrets=[VIRUSTOTAL_API_KEY])
def newentry(event: Event[DocumentSnapshot | None]) -> None:
    """Listens for new documents to be added to /messages. If the document has
    an "text" field, it does some checking of it """

    # Get the value of "original" if it exists.
    if event.data is None:
        return
    try:
        new_value = event.data.to_dict()
        api_key = VIRUSTOTAL_API_KEY.value
        print(vt_lookup(api_key,new_value['text']))
    except KeyError:
        # No "text" field, so do nothing.
        return
    
    def vt_lookup(api_key, url):
        url = "https://www.virustotal.com/api/v3/urls"

        payload = { "url": url }
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
            return f"Went wrong {response.status_code}"

        # from the response we can get the link to the actual scan
        scan_response = requests.get(response_json['data']['links']['self'], headers=headers)
        if scan_response.status_code == 200:
            scan_response_json = json.loads(scan_response.text)
            return scan_response_json
        else:
            return f"Something went wrong {scan_response.status_code}"
            
    # event.data.reference.update({"vt-score": "90%"})

