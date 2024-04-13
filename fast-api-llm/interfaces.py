from pydantic import BaseModel


class Query(BaseModel):
    query: str
    user: str
    model_name:  str = "default"


class TrainBody(BaseModel):
    model_key:str
    file_path:str