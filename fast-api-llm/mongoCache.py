from pymongo import MongoClient
import _pickle as pickle # type: ignore
from functools import lru_cache
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time

class MongoCacheManager: 
    def __init__(self, db_name, collection_name, uri):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save(self, key, data):
        """Save data to MongoDB."""
        # Serialize data to a binary format using pickle
        try:
            serialized_data = pickle.dumps(data)
            self.collection.update_one({'_id': key}, {'$set': {'data': serialized_data}}, upsert=True)
            # fetch and store in cache to avoid cache cold start
            self.load(key) 
        except TypeError as e:
            print(f"Error saving data to Store: {e}")

    @lru_cache(maxsize=128)
    def load(self, key):
        """Load data from MongoDB."""
        print("fetched from store")
        document = self.collection.find_one({'_id': key})
        if document and 'data' in document:
            return pickle.loads(document['data'])
        return None

# UNit test code - Usage example
if __name__ == '__main__':
    import os
    from dotenv import load_dotenv 
    load_dotenv() 

    db_uri = os.getenv("MONGO_CONNECT")
    db_name= os.getenv("MONGO_DB_NAME")
    collection_name= os.getenv("MONGO_COLLECTION_NAME")
    cache_manager = MongoCacheManager(uri=db_uri, collection_name=collection_name, db_name=db_name)

    # Save data
    # data_to_cache = {'example_key': 'example_value'}
    # cache_manager.save('example_data_key', data_to_cache)

    # # Load data
    # key1 = " yashgunjal98@gmail.com"
    # key2 = " model2"
    # retrieved_data = cache_manager.load('example_data_key')
    
    # print(" ---------------again")
    # retrieved_data = cache_manager.load('example_data_key')
    # print(retrieved_data)



    ### load time test
    key1 = "yashgunjal98@gmail.com"
    key2 = "model2"
    print(" fetch initiate")
    start1 = time.time()

    retrieved_data = cache_manager.load(key1)
    end1 = time.time()
    print(" first call",end1-start1)
    print(" second fetch initiate")

    start2 = time.time()
    retrieved_data = cache_manager.load(key1)
    end2 = time.time()
    print(" second call",end2-start2)

