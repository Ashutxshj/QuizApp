import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase service account key JSON file
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

# Get Firestore instance
db = firestore.client()