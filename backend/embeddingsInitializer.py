from langchain_aws import BedrockEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_KEY_REGION = os.getenv('AWS_KEY_REGION')

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["demo_rag_insurance"]
collection = db["claims_final"]

embeddings_client = BedrockEmbeddings(model_id="cohere.embed-english-v3",
                                      region_name=AWS_KEY_REGION,
                                      credentials_profile_name="ask-leafy"
                                      )


for doc in collection.find():    
    text = doc["claimDescription"]
    embedding = embeddings_client.embed_query(text)
    collection.update_one({"_id": doc["_id"]}, {"$set": {"claimDescriptionEmbeddingCohere": embedding}})