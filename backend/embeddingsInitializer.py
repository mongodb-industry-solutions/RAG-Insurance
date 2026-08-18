"""
Backfills claimDescriptionEmbeddingCohere on every document in claims_final that
doesn't already have it, using AWS Bedrock's cohere.embed-english-v3 model.

Safe to run again: skips documents that already have the field.

Usage:
    poetry run python embeddingsInitializer.py
"""

from langchain_aws import BedrockEmbeddings
from pymongo import MongoClient
from dotenv import load_dotenv
from bedrock_client import BedrockClient
import os

load_dotenv()

AWS_KEY_REGION = os.getenv("AWS_KEY_REGION")
APP_NAME = "devrel-demo-fastapi-bedrock-insurance-rag"

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri, appname=APP_NAME)
db = client["demo_rag_insurance"]
collection = db["claims_final"]

bedrock_client = BedrockClient(region_name=AWS_KEY_REGION)._get_bedrock_client()
embeddings_client = BedrockEmbeddings(
    client=bedrock_client,
    model_id=os.getenv("BEDROCK_MODEL_COHERE_EMBED", "cohere.embed-english-v3"),
)


def main():
    pending = list(collection.find({"claimDescriptionEmbeddingCohere": {"$exists": False}}))
    if not pending:
        print("Every document already has claimDescriptionEmbeddingCohere, nothing to do.")
        return

    for doc in pending:
        text = doc["claimDescription"]
        embedding = embeddings_client.embed_query(text)
        collection.update_one({"_id": doc["_id"]}, {"$set": {"claimDescriptionEmbeddingCohere": embedding}})
        print(f"Embedded {doc['_id']}")

    print(f"Done. Embedded {len(pending)} document(s).")


if __name__ == "__main__":
    main()