from langchain_aws import BedrockEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv
from bedrock_client import BedrockClient
import os
load_dotenv()

AWS_KEY_REGION = os.getenv('AWS_KEY_REGION')

mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri, appName="rag-insurance")
db = client["demo_rag_insurance"]
collection = db["claims_final"]

bedrock_client = BedrockClient(region_name=AWS_KEY_REGION)._get_bedrock_client()

embeddings_client = BedrockEmbeddings(client=bedrock_client,
                                      model_id=os.getenv("BEDROCK_MODEL_COHERE_EMBED", "cohere.embed-english-v3")
                                      )


for doc in collection.find():    
    text = doc["claimDescription"]
    embedding = embeddings_client.embed_query(text)
    collection.update_one({"_id": doc["_id"]}, {"$set": {"claimDescriptionEmbeddingCohere": embedding}})