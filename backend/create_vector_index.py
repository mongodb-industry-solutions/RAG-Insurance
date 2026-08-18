"""
Creates the vector_index_claim_description_cohere MongoDB Vector Search index on
claims_final.claimDescriptionEmbeddingCohere, using langchain-mongodb's
create_vector_search_index helper (the current `type: "vectorSearch"` index
format, not the older Search index with a knnVector field mapping).

Run this once, after the claims_final collection has documents with a
claimDescriptionEmbeddingCohere field (see embeddingsInitializer.py).

Usage:
    poetry run python create_vector_index.py
"""

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb.index import create_vector_search_index

load_dotenv()

INDEX_NAME = "vector_index_claim_description_cohere"
EMBEDDING_PATH = "claimDescriptionEmbeddingCohere"
EMBEDDING_DIMENSIONS = 1024  # cohere.embed-english-v3's output dimensionality
APP_NAME = "devrel-demo-fastapi-bedrock-insurance-rag"


def main():
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise SystemExit("MONGO_URI must be set (see .env)")

    client = MongoClient(mongo_uri, appname=APP_NAME)
    collection = client["demo_rag_insurance"]["claims_final"]

    existing = {idx["name"] for idx in collection.list_search_indexes()}
    if INDEX_NAME in existing:
        print(f"Index '{INDEX_NAME}' already exists on claims_final, skipping.")
        client.close()
        return

    create_vector_search_index(
        collection=collection,
        index_name=INDEX_NAME,
        path=EMBEDDING_PATH,
        dimensions=EMBEDDING_DIMENSIONS,
        similarity="cosine",
        wait_until_complete=120,
    )
    print(f"'{INDEX_NAME}' is READY and queryable.")
    client.close()


if __name__ == "__main__":
    main()
