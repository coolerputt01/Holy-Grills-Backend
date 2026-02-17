import firebase_admin
from firebase_admin import credentials, firestore

app_credentials = credentials.Certificate("sk.json")
firebase_admin.initialize_app(app_credentials)

db = firestore.client()
