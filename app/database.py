import motor.motor_asyncio
from decouple import config

def connect_db():
    DATABASE_URL = config("DATABASE_URL")
    DATABASE_NAME = "bookshop"
   # client = pymongo.MongoClient(DATABASE_URL)

    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    db = client[DATABASE_NAME]
    collection = db["books"]
    
    print('🚀 Connected to MongoDB...')
    return collection
