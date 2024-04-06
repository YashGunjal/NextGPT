from typing import Union
from typing import Annotated

from fastapi import FastAPI,Header

from interfaces import Query

from model import ModelManager
from storewithcache import CacheManager



app = FastAPI()


cache_manager = CacheManager()
model_manager = ModelManager(cache_manager)

# Example usage
document = "Example document for training."
model = model_manager.train_model(document)
model_key = "model_key"

model_manager.save_model(model_key, model)
response = model_manager.use_model(model_key, "New document for prediction.")
print(response)





@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/query")
def read_item( query: Query, user_agent: Annotated[str | None, Header()] = None ):
    return { "query": query.query, "status": "success" }
