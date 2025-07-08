from pymongo import MongoClient
import os

MONGODB_URL=os.getenv("DB_URL")
DB_NAME=os.getenv("DB_NAME")

mongo_client=MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
db = mongo_client[DB_NAME]

users_collection=db["users"]
books_collection=db["books"]