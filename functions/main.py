from firebase_admin import initialize_app
from firebase_functions.firestore_fn import (
  on_document_created,
  Event,
  DocumentSnapshot,
)

initialize_app()
#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")

@on_document_created(document="users/{userId}")
def myfunction(event: Event[DocumentSnapshot]) -> None:
  # Get a dictionary representing the document
  # e.g. {'name': 'Marie', 'age': 66}
  new_value = event.data.to_dict()

  # Access a particular field as you would any dictionary
  name = new_value["name"]

  # Perform more operations ...