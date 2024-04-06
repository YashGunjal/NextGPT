import redis
import json
from llama_index.packs.subdoc_summary import SubDocSummaryPack

# Initialize Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Assuming you have an instance of SubDocSummaryPack
summary_pack = SubDocSummaryPack()

# Serialize and store data
user_id = 'user_123'  # Unique identifier for the user/session
serialized_data = json.dumps(summary_pack.to_dict())  # Convert to dict and serialize
r.set(user_id, serialized_data)

# Retrieve and deserialize data
retrieved_data = r.get(user_id)
if retrieved_data:
    summary_pack = SubDocSummaryPack.from_dict(json.loads(retrieved_data))
