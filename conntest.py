import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    mongo_uri = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(mongo_uri)

    try:
        # Try to list the databases
        dbs = await client.list_database_names()
        print("Connected to MongoDB Atlas. Databases:", dbs)
    except Exception as e:
        print("Failed to connect to MongoDB Atlas:", str(e))

if __name__ == "__main__":
    asyncio.run(test_connection())