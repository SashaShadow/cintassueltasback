from pymongo import MongoClient
from local_config import *

def get_mongo_db():
    mongo_uri = f"{mongo_db_uri}"

    try:
        client = MongoClient(mongo_uri)  
        db = client["cintassueltas"] 
        return db
    except Exception as e:
        return None