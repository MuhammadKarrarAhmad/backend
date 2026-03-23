from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["glh_database"]
users_collection = db["users"]