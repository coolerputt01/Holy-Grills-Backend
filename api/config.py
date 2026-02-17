import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


firebase_key = os.environ.get("FIREBASE_KEY")
cred_dict = json.loads(firebase_key)
app_credentials = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(app_credentials)

db = firestore.client()
