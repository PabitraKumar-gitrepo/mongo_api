from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient  ## this is  MONGODB driver 
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI="mongodb://localhost:27017/"    ### local instance MongoDB
###MONGO_URI='mongodb+srv://pabi:Pabi1234@cluster-1.hq2achw.mongodb.net/?appName=Cluster-1'
#MONGO_URI=os.getenv("MONGO_URI") ##from .env file 
client=AsyncIOMotorClient(MONGO_URI)  ## MongoDB connection
db=client["demodb"]
db_coll=db["demo_coll"]

#print ("db name:",db)
#print ("coll name:",db_coll)
##default_db=client.get_default_database()
##print ("default db name:",default_db)

app=FastAPI()

class coll_data(BaseModel):
    name:str
    phone:int
    city:str
    course:str


@app.post("/testapimongodb/insert")
async def coll_data_insert_helper(data:coll_data):
    try:
        # Insert data into MongoDB
        result = await db_coll.insert_one(data.dict())
        # Return a response containing the inserted id
        return {"inserted_id": str(result.inserted_id), "message": "Record inserted successfully."}
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    #result=await db_coll.insert_one(data.dict())
    #return str(result.inserted_id)

## to remove _id from mongodb (its generated from insert function while inserting data to collection)
def remove_id_helper(doc):
    doc["id"]=str(doc["_id"])
    del doc["_id"]
    return doc



@app.get("/testapimongodb/getdata")
async def get_coll_data():
    items=[]
    cursor=db_coll.find({})
    async for document in cursor:
        items.append(remove_id_helper(document))
    return items




