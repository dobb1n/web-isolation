from firebase_functions.firestore_fn import (
  on_document_created,
  on_document_deleted,
  on_document_updated,
  on_document_written,
  Event,
  Change,
  DocumentSnapshot,
)

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore

app = initialize_app()

@on_document_created(document="messages/{docID}", region="europe-west2")
def newentry(event: Event[DocumentSnapshot | None]) -> None:
    """Listens for new documents to be added to /messages. If the document has
    an "text" field, it does some checking of it """

    # Get the value of "original" if it exists.
    if event.data is None:
        return
    try:
        url = event.data.get("text")
    except KeyError:
        # No "text" field, so do nothing.
        return

    # Set the "uppercase" field.
    print(f"Checking virus total for {event.params['docID']}: {text}")
    
    event.data.reference.update({"vt-score": "90%"})
