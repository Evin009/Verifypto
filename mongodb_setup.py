
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection string
CONNECTION_STRING = "mongodb+srv://TheLegoMax:3SIrQKvUtK08kPtx@crypto-cluster.0umlksj.mongodb.net/?retryWrites=true&w=majority&appName=Crypto-Cluster"

client = MongoClient(CONNECTION_STRING)
db = client['crypto_verification']
collection = db['verifications']

def save_verification(report, user_email=None, user_uid=None):
    report["timestamp"] = datetime.utcnow()
    if user_email:
        report["user_email"] = user_email
    if user_uid:
        report["user_uid"] = user_uid
    return collection.insert_one(report)
    
def get_all_verifications():
    return list(collection.find({}, {"_id": 0}))

def get_by_wallet(wallet_address):
    return list(collection.find({"wallet": wallet_address}).sort("timestamp", -1))

# ✅ ADD THIS FUNCTION to fix your error:
def get_by_user(email):
    return list(collection.find({"user_email": email}).sort("timestamp", -1))

# Optional leaderboard function:
def get_top_riskiest(limit=5):
    return list(collection.find().sort("risk_score", -1).limit(limit))
