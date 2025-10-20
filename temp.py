from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://arbazubairy:Imran%40123@charminar.gdqxafh.mongodb.net/?retryWrites=true&w=majority&appName=charMinar"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.mydatabase  # replace with your DB name
collection = db.mycollection

# Insert a document
collection.insert_one({"name": "Arbaz", "role": "developer"})

# Find documents
for doc in collection.find():
    print(doc)