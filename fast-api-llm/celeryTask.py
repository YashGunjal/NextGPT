import time
from celery import Celery
import os
from dotenv import load_dotenv 
load_dotenv() 

from managers_init import SubModel
from fileManager import FileManagerS3

redis_url=os.getenv("EC2_REDIS")
s3_access=os.getenv("AWS_ACCESS_KEY")
s3_secret=os.getenv("AWS_SECRET_KEY")
bucket_name= os.getenv("S3_BUCKET_NAME")

celery = Celery(
    "model_tasks",
    broker=redis_url,
    backend=redis_url
)

@celery.task
def train_model(model_key, file_path):
    # get documents
    print(model_key, file_path)
    file_manager = FileManagerS3(aws_access=s3_access, aws_secret=s3_secret, bucket_name=bucket_name)
    file_path = file_path 
    document = file_manager.get_file(file_path)
    # train Model
    new_model = SubModel.train_model(document)
    SubModel.save_model(model_key, new_model)
    return "model_key"


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

