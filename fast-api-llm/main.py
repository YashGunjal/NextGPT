from typing import Union
from typing import Annotated

from fastapi import FastAPI, Header
from interfaces import Query, TrainBody

from managers_init import SubModel
from celeryTask import train_model

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/api/v1/train")
def read_item(train_data: TrainBody):
    train_model.delay(train_data.model_key, train_data.file_path)
    return {"response": "success"} 

@app.post("/api/v1/query")
def read_item( query: Query, user_agent: Annotated[str | None, Header()] = None ):
    model_key = query.user  if query.user else "yashgunjal98@gmail.com"
    response = SubModel.use_model(model_key, query.query )
    print(response)
    return  response

