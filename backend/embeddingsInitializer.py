from langchain_aws import BedrockEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["demo_rag_insurance"]
collection = db["claims_final"]

embeddings_client = BedrockEmbeddings(model_id="cohere.embed-english-v3")


for doc in collection.find():    
    text = doc["claimDescription"]
    embedding = embeddings_client.embed_query(text)
    collection.update_one({"_id": doc["_id"]}, {"$set": {"claimDescriptionEmbeddingCohere": embedding}})