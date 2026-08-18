# Insurance RAG demo

Claim management with LLMs in RAG and vector search | MongoDB

## Instructions

Create a file named `backend/.env` with your AWS region and MongoDB connection string:

```bash
AWS_KEY_REGION=<your aws region>
MONGO_URI="<your mongodb atlas connection string>"
```

AWS credentials are resolved through the standard boto3 chain (an `AWS_PROFILE` env var pointing at an SSO profile works, as does `aws configure`) — this repo does not read AWS access keys from `.env`.

The application uses AWS Bedrock with the following models:
- **Embeddings**: Cohere Embed English v3 (`cohere.embed-english-v3`)
- **LLM**: Anthropic Claude Haiku 4.5 (`us.anthropic.claude-haiku-4-5-20251001-v1:0`)

## Setup Instructions

### Prerequisites
- AWS Account with Bedrock access
- A **MongoDB Atlas cluster**. If you don't have one yet, [sign up for free and deploy an M0 cluster](https://www.mongodb.com/cloud/atlas/register?utm_campaign=devrel&utm_source=github&utm_medium=referral&utm_content=insurance_rag_demo&utm_term=learning.fuel).
- Python 3.10, 3.11, or 3.12 (see `backend/pyproject.toml`)
- Node.js and npm

## Run it Locally

### Backend

1. From the repo root:
   ```bash
   cd backend
   poetry install
   ```
2. In MongoDB Atlas, create a database called `demo_rag_insurance` and a collection called `claims_final`, then import `data/demo_rag_insurance.claims.json` into it (Compass or `mongoimport` both handle the Extended JSON `$oid` fields correctly).
3. The imported documents don't include Cohere embeddings yet — generate them:
   ```bash
   poetry run python embeddingsInitializer.py
   ```
   Safe to run again — it only embeds documents that don't already have `claimDescriptionEmbeddingCohere`.
4. Create the vector search index (must run after step 3, since the field has to exist on at least one document first):
   ```bash
   poetry run python create_vector_index.py
   ```
   This creates a modern `vectorSearch`-type index named `vector_index_claim_description_cohere` on `claims_final.claimDescriptionEmbeddingCohere` (1024 dimensions, cosine similarity) — not the older Search-index-with-a-knnVector-field-mapping style. Safe to run again. Prefer the Atlas UI instead? Use the same field definition:
   ```json
   {
     "fields": [
       {
         "type": "vector",
         "path": "claimDescriptionEmbeddingCohere",
         "numDimensions": 1024,
         "similarity": "cosine"
       }
     ]
   }
   ```
5. Start the backend server:
   ```bash
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000
   ```

**_Note:_** The server will be running on `http://localhost:8000`.

#### API Documentation

You can access the API documentation by visiting the following URL:

```
http://localhost:<PORT_NUMBER>/docs
```
E.g. `http://localhost:8000/docs`

### To connect with Frontend

### Configure the Environment Variables for the frontend (optional)

The frontend's `/api/askTheLlm` route proxies to the backend at `http://localhost:8000` by default — no configuration needed for local dev against a backend on the default port. To point at a different backend, create `frontend/.env.local`:

```bash
INTERNAL_API_URL="http://localhost:8000"
```

### Run the Frontend
1. Navigate to the `frontend` folder.
2. Install dependencies by running:
```bash
npm install
```
3. Start the frontend development server with:
````bash
npm run dev
````

The frontend will now be accessible at http://localhost:8080 by default, providing a user interface to interact with the insurance claims RAG demo.

## Run with Docker (Preferred)

Prerequisites:
- Docker Desktop installed on your machine.
- Docker Desktop running on your machine.

### Docker Setup Instructions

To run the application using Docker, follow these setup steps:

### Build the Application
> **_NOTE:_** If you don’t have make installed, you can install it using `sudo apt install make` or `brew install make`

1. To run with Docker use the following command:
```
make build
```
2. To delete the container and image run:
```
make clean
```
## Common errors

- Check that you've created an `.env` file that contains your valid (and working) API keys, environment and index variables.
- AWS CLI configured with appropriate credentials

You can request model access through the AWS Bedrock console if needed.
