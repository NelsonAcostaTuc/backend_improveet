from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://mongo:27017/")

client = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_DETAILS)

async def get_database():
    return client.get_database("user_db")  # Se crea 'user_db' si no existe

async def close_mongo_connection():
    client.close()
