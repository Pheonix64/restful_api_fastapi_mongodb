import motor.motor_asyncio
from decouple import config

def connect_db():
    DATABASE_URL = config("DATABASE_URL") #"mongodb+srv://libraire:Azval227@clusterbooks.fdeazkj.mongodb.net/?retryWrites=true&w=majority"
    # client = pymongo.MongoClient(DATABASE_URL)
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL) 
    print('🚀 Connected to MongoDB...')
    return client                                 
