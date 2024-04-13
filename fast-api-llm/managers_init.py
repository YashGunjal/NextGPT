import os
from dotenv import load_dotenv 
from modelManager import ModelManager 
from mongoCache import MongoCacheManager

load_dotenv() 

db_uri = os.getenv("MONGO_CONNECT")
db_name= os.getenv("MONGO_DB_NAME")
collection_name= os.getenv("MONGO_COLLECTION_NAME")
redis_url=os.getenv("EC2_REDIS")

# intilaising managers 
CacheManager = MongoCacheManager(db_name= db_name, uri= db_uri, collection_name=collection_name)
SubModel = ModelManager(CacheManager)