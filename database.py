from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["GLH_DB"]

users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]
loyalty_collection = db["loyalty"]