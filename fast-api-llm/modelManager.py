from llama_index.packs.subdoc_summary import SubDocSummaryPack
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.core import SimpleDirectoryReader
from mongoCache import MongoCacheManager
import os
from dotenv import load_dotenv 
load_dotenv() 

llmAPi = HuggingFaceInferenceAPI(
    model_name="mistralai/Mistral-7B-Instruct-v0.2"
)

embed_model_HGGF = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

class ModelManager:
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
    
    def train_model(self, documents):
        """Train your model with the given document."""
        subdoc_summary_pack = SubDocSummaryPack(
            documents,
            verbose=True,
            parent_chunk_size=8192,  # default,
            child_chunk_size=512,  # default
            llm=llmAPi,
            embed_model=embed_model_HGGF,
        )
        return subdoc_summary_pack
    
    def save_model(self, key, model):
        """Save model to cache and Mongo store."""
        self.cache_manager.save(key, model)
    
    def get_model(self, key):
        """Fetch the model from cache or mongo"""
        model = self.cache_manager.load(key)
        return model
    
    def use_model(self, key, query):
        """Use the model for some operation, e.g., prediction."""
        model = self.get_model(key)
        if not model:
            return "Model not found."
         
        response = model.run(query)
        return response
    

if __name__ == '__main__':
    from timeit import default_timer as timer
    import time
    db_uri = os.getenv("MONGO_CONNECT")
    cache_manager = MongoCacheManager(uri = db_uri)
    model_manager = ModelManager(cache_manager=cache_manager)
    print(" initilisation done")

    # Save data
    ###### test set 1
    # gets documents
    test_key = "model2"
    # documents = SimpleDirectoryReader("test-files2").load_data()
    # process 
    # new_model = model_manager.train_model(documents=documents)

    # make mode and save it
    # model_manager.save_model(key=test_key, model=new_model)

    # use model

    start2 = time.time()
    atrat12 = timer()
    print(model_manager.use_model(key="model2", query="what are the attention mechanism used"))
    end2 = time.time()
    end12 = timer()
    print(end2-start2)
    print(end12 -atrat12)

    print(" second output")
    # print(model_manager.use_model(key=test_key, query="why self attention"))




    ##### test set_2

    # documents = SimpleDirectoryReader("test-files2 ").load_data()
    # process 
    # new_model = model_manager.train_model(documents=documents)

    # make mode and save it
    # model_manager.save_model(key=test_key, model=new_model)

    # use model

    # print(model_manager.use_model(key=test_key, query="what are encoders and decoders"))
    print(" second output")

