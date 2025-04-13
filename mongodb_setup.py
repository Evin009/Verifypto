from pymongo import MongoClient
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://TheLegoMax:3SIrQKvUtK08kPtx@crypto-cluster.0umlksj.mongodb.net/?retryWrites=true&w=majority&appName=Crypto-Cluster"

client = MongoClient(CONNECTION_STRING)
db = client['crypto_verification']
collection = db['verifications']

def save_verification(report):
    report["timestamp"] = datetime.utcnow()
    return collection.insert_one(report)

def get_all_verifications():
    return list(collection.find())

def get_by_wallet(wallet_address):
    return list(collection.find({"wallet": wallet_address}))
