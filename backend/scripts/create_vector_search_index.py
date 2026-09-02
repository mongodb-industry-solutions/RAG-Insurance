"""
Idempotent creation of the MongoDB Atlas Vector Search index that ask_llm.py's
vector_store depends on (ATLAS_VECTOR_SEARCH_INDEX_NAME =
"vector_index_claim_description_cohere"). Run this once against the claims_final
collection before relying on RAG retrieval.

Usage:
    poetry run python scripts/create_vector_search_index.py
"""

import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

INDEX_NAME = "vector_index_claim_description_cohere"
VECTOR_FIELD = "claimDescriptionEmbeddingCohere"
DIMENSIONS = 1024
SIMILARITY_METRIC = "cosine"
DB_NAME = "demo_rag_insurance"
COLLECTION_NAME = "claims_final"

def create_index(
    index_name: str = INDEX_NAME,
    vector_field: str = VECTOR_FIELD,
    dimensions: int = DIMENSIONS,
    similarity_metric: str = SIMILARITY_METRIC,
) -> dict:
    mongo_uri = os.getenv("MONGODB_URI")

    client = MongoClient(mongo_uri, appName="rag-insurance")
    collection = client[DB_NAME][COLLECTION_NAME]

    index_config = {
        "name": index_name,
        "type": "vectorSearch",
        "definition": {
            "fields": [
                {
                    "path": vector_field,
                    "type": "vector",
                    "numDimensions": dimensions,
                    "similarity": similarity_metric,
                }
            ]
        },
    }

    logger.info(f"Collection: {DB_NAME}.{COLLECTION_NAME}")
    logger.info(f"Vector Field: {vector_field}")
    logger.info(f"Dimensions: {dimensions}")
    logger.info(f"Similarity Metric: {similarity_metric}")

    try:
        collection.create_search_index(index_config)
        logger.info(f"Vector search index '{index_name}' created successfully.")
        return {"status": "success", "message": f"Vector search index '{index_name}' created successfully."}
    except OperationFailure as e:
        if e.code == 68:  # IndexAlreadyExists
            logger.info(f"Vector search index '{index_name}' already exists.")
            return {"status": "info", "message": f"Vector search index '{index_name}' already exists."}
        logger.error(f"Error creating vector search index: {e}")
        return {"status": "error", "message": f"Error creating vector search index: {e}"}

if __name__ == "__main__":
    result = create_index()
    print(result)
