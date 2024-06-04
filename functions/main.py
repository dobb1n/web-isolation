from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore

from firebase_admin import initialize_app
from firebase_functions.firestore_fn import (
  on_document_created,
  Event,
  DocumentSnapshot,
)

initialize_app()

@on_document_created(document="messages/{text}")
def myfunction(event: Event[DocumentSnapshot]) -> None:
  # Get a dictionary representing the document
  # e.g. {'name': 'Marie', 'age': 66}
  new_value = event.data.to_dict()

  # Access a particular field as you would any dictionary
  url = new_value["text"]
  print(url)
  # Perform more operations ...
