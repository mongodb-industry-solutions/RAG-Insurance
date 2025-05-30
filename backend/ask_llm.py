from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_aws import BedrockEmbeddings, ChatBedrock
from pymongo import MongoClient
from dotenv import load_dotenv
from bedrock_client import BedrockClient
import json
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI
mdb_uri = os.getenv("MONGO_URI")
client = MongoClient(mdb_uri)
AWS_KEY_REGION = os.getenv("AWS_KEY_REGION")

# Set database and collection names
DB_NAME = "demo_rag_insurance"
COLLECTION_NAME = "claims_final"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index_claim_description_cohere"

# Getting Bedrock Client
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
bedrock_client = BedrockClient(
    region_name=AWS_KEY_REGION
)._get_bedrock_client()

# Initialize BedrockEmbeddings with AWS credentials and region
embeddings = BedrockEmbeddings(
    client=bedrock_client,
    model_id="cohere.embed-english-v3"
)

# Initialize MongoDB Atlas Vector Search
vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    text_key="claimDescription",
    embedding_key="claimDescriptionEmbeddingCohere",
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

def vector_search(question):
    
    semantic_search_results = vector_store.similarity_search(question, k=3)
    for res in semantic_search_results:
        del res.metadata['damageDescriptionEmbedding']
        del res.metadata['_id']
        del res.metadata['photoEmbedding']
        if 'claimDescriptionEmbedding' in res.metadata:
            del res.metadata['claimDescriptionEmbedding']
    
    return semantic_search_results

def ask_llm(question, semantic_search_results):
    
    llm = ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        region=AWS_KEY_REGION
    )

    # Create the body with the new question
    body = {
        "Additional Information": str(semantic_search_results),
        "Instructions": "Be brief and don't go through too many steps",
        "message": question
    }

    input_text = json.dumps(body)

    return llm.invoke(input_text).content

def retrieval(question):
    
    search_results = vector_search(question)
    response = ask_llm(question, search_results)
    return search_results, response

