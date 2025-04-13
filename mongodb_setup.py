from pymongo import MongoClient

# Replace <username>, <password>, and <dbname> with your MongoDB Atlas credentials
CONNECTION_STRING = "mongodb+srv://TheLegoMax:3SIrQKvUtK08kPtx@crypto-cluster.0umlksj.mongodb.net/?retryWrites=true&w=majority&appName=Crypto-Cluster"
# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)

# Create or access a database
db = client['crypto_verification']

# Create or access a collection
collection = db['transactions']

# Insert sample data
sample_data = {
    "transaction_id": "tx12345",
    "wallet_address": "0xABC123DEF456",
    "amount": 0.5,
    "currency": "BTC",
    "timestamp": "2025-04-13T12:00:00Z",
    "status": "pending"
}
collection.insert_one(sample_data)

# Retrieve and print all documents in the collection
for transaction in collection.find():
    print(transaction)