from pymongo import MongoClient
import pickle
from functools import lru_cache



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

class MongoCacheManager:
    def __init__(self, db_name='cacheDB', collection_name='cacheCollection', uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        print("connection done", db_name, collection_name)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    @lru_cache(maxsize=128)
    def get_from_cache(self, key):

        print("fetched from store")
        model_obj = self.collection.find_one({'_id': key})
        return  model_obj

    def save(self, key, data):
        """Save data to MongoDB."""
        # Serialize data to a binary format using pickle
        serialized_data = pickle.dumps(data)
        # Save or update the document with the given key
        print(" stored, data",serialized_data)

        try:
            serialized_data = pickle.dumps(data)
            self.collection.update_one({'_id': key}, {'$set': {'data': serialized_data}}, upsert=True)
            # fetch and store in cache
            self.get_from_cache(key) 
        except TypeError as e:
            print(f"Error saving data to Redis: {e}")

    def load(self, key):
        """Load data from MongoDB."""
        cache_data = self.get_from_cache(key) 
        if cache_data:
            return pickle.loads(cache_data['data'])

        document = self.collection.find_one({'_id': key})
        print("  fetched data", document)
        if document and 'data' in document:
            # Deserialize data from binary format
            return pickle.loads(document['data'])
        return None

# Usage example

if __name__ == '__main__':
    cache_manager = MongoCacheManager(uri=uri)

    # Save data
    data_to_cache = {'example_key': 'example_value'}
    cache_manager.save('example_data_key', data_to_cache)

    # Load data
    retrieved_data = cache_manager.load('example_data_key')
    print(" ---------------again")
    retrieved_data = cache_manager.load('example_data_key')
    print(retrieved_data)
