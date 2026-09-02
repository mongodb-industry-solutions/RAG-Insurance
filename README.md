# Insurance RAG demo

Claim management with LLMs in RAG and vector search | MongoDB

## Where MongoDB Shines?

[MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register?utm_campaign=devrel&utm_source=github&utm_medium=referral&utm_content=rag_insurance&utm_term=learning.fuel) stores insurance claim documents and their vector embeddings side by side in a single collection. [Atlas Vector Search](https://www.mongodb.com/products/platform/atlas/vector-search?utm_campaign=devrel&utm_source=github&utm_medium=referral&utm_content=rag_insurance&utm_term=learning.fuel) retrieves the claims most semantically similar to a user's question, which are then passed to an LLM to produce a grounded answer.

## Instructions

Create a file named `backend/.env` and store your AWS credentials and MongoDB connection string in it, following this format:

```bash
AWS_PROFILE=<your aws profile>
AWS_KEY_REGION=<your aws region>
MONGODB_URI=""
```

In MongoDB Atlas create a database called "demo_rag_insurance" and a collection called "claims_final", then import the dataset into it:

```bash
mongoimport --uri "<your MONGODB_URI>" --db demo_rag_insurance --collection claims_final --file data/demo_rag_insurance.claims.json --jsonArray
```

The imported documents don't carry Cohere embeddings yet — generate them by running, from `backend/`:

```bash
poetry run python embeddingsInitializer.py
```

Then create the Vector Search index for "claimDescriptionEmbeddingCohere" (named "vector_index_claim_description_cohere") by running:

```bash
poetry run python scripts/create_vector_search_index.py
```

The application uses AWS Bedrock with the following models (overridable via `BEDROCK_MODEL_HAIKU` / `BEDROCK_MODEL_COHERE_EMBED`):
- **Embeddings**: Cohere Embed English v3 (`cohere.embed-english-v3`)
- **LLM**: Claude Haiku 4.5 (`us.anthropic.claude-haiku-4-5-20251001-v1:0`)

## Setup Instructions

### Prerequisites
- AWS Account with Bedrock access
- A [MongoDB Atlas cluster](https://www.mongodb.com/cloud/atlas/register?utm_campaign=devrel&utm_source=github&utm_medium=referral&utm_content=rag_insurance&utm_term=learning.fuel)
- Python 3.10 - 3.12
- Node.js 18.17+ and npm

## Run it Locally

### Backend

1. Navigate to the `backend` folder.
2. Configure Poetry to use an in-project virtualenv and install dependencies:
   ```bash
   poetry config virtualenvs.in-project true
   poetry install
   ```
3. Verify that the `.venv` folder has been generated within the `/backend` directory.
4. Make sure to select the Python interpreter from the `.venv` folder. You can change this in Visual Studio Code by clicking on the Python version in the bottom left corner, or searching by `Python: Select Interpreter` in the command palette. For this project, the Python interpreter should be located at `./backend/.venv/bin/python`.

### Interact with the API

Start the server by running the following commands:
   1. Make sure to be over `/backend` directory. 
        ```bash
         cd backend
         ```
   3. Start the backend server with the following command:
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

### Configure the Environment Variables for the frontend

1. In the `frontend` folder, create a `.env.local` file.
2. Add the URL for the API using the following format:

```bash
NEXT_PUBLIC_ASK_LEAFY_API_URL=http://localhost:8000/askTheLlm
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

The frontend will now be accessible at http://localhost:8080 by default, providing a user interface to interact with the claim RAG demo.

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
