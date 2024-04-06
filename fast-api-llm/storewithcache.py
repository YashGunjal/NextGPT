from functools import lru_cache
import redis
import json
import pickle
from upstash_redis import Redis


redis_host='immense-hamster-30483.upstash.io',
redis_port=30483,
ssl=True


class CacheManager:
    def __init__(self, redis_host='localhost', redis_port=30483, password="" , redis_db="llm-store"):
        # self.redis = redis.Redis(host=redis_host, port=redis_port, password=password, ssl=True,  )
        self.redis = Redis(url="", token="")
    
    @lru_cache(maxsize=128)
    def get_from_cache(self, key):
        """Try to get data from in-memory cache"""
        print("fetched from redis")
        model_obj = self.redis.get(key)
        return  model_obj
    
    def get(self, key):
        """Try to get data from Redis store"""
        try:
            data = self.get_from_cache(key)  

            if not data:
                print("no response from cache,fetchfrom redis",  data)
                data = self.redis.get(key)

            if data:
                return pickle.loads(data)
            return None
        except TypeError as e:
            print(f"Error loading data from Redis: {e}")
            return None
        #
       

    
    def save(self, key, data):
        """Save data to both in-memory cache and Redis"""
        # Update in-memory cache

        try:
            serialized_data = pickle.dumps(data)
            print(" serilaised data", serialized_data, type(serialized_data))
            self.redis.set(key, json.dumps(serialized_data))
            self.get_from_cache(key) 
        except TypeError as e:
            print(f"Error saving data to Redis: {e}")
        # Save to Redis







if __name__ == '__main__':
    # test fro cache_manager
    RedisCache = CacheManager(redis_host, redis_port, password)
    print("----------------made connection")
    RedisCache.save("key","some data")
    print(RedisCache.get('key'))
    print("----------------again")
    print(RedisCache.get("key"))
    print("----------------Done!")
    