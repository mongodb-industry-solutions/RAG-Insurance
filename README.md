# Insurance RAG demo

Claim management with LLMs in RAG and vector search | MongoDB

## Instructions

Create a file named '.env' and store your AWS credentials and MongoDB connection string in it, follow this format:

```bash
AWS_KEY_REGION=<your aws region>
MONGO_URI=""
```

In MongoDB Atlas create a database called "demo_rag_insurance" and a collection called "claims_final", import the dataset "demo_rag_insurance.claims.json" into the collection. You have to create a Vector Search Index for "claimDescriptionEmbeddingCohere" called "vector_index_claim_description_cohere":

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

The application uses AWS Bedrock with the following models:
- **Embeddings**: Cohere Embed English v3 (`cohere.embed-english-v3`)
- **LLM**: Anthropic Claude 3 Haiku (`anthropic.claude-3-haiku-20240307-v1:0`)

## Setup Instructions

### Prerequisites
- AWS Account with Bedrock access
- MongoDB Atlas cluster
- Python 3.8+
- Node.js and npm

## Run it Locally

### Backend

1. (Optional) Set your project description and author information in the `pyproject.toml` file:
   ```toml
   description = "Your Description"
   authors = ["Your Name <you@example.com>"]
2. Open the project in your preferred IDE (the standard for the team is Visual Studio Code).
3. Open the Terminal within Visual Studio Code.
4. Ensure you are in the root project directory where the `makefile` is located.
5. Execute the following commands:
  - Poetry start
    ````bash
    make poetry_start
    ````
  - Poetry install
    ````bash
    make poetry_install
    ````
6. Verify that the `.venv` folder has been generated within the `/backend` directory.
7. Make sure to select the Python interpreter from the `.venv` folder. You can change this in Visual Studio Code by clicking on the Python version in the bottom left corner, or searching by `Python: Select Interpreter` in the command palette. For this project, the Python interpreter should be located at `./backend/.venv/bin/python`.

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
NEXT_PUBLIC_ASK_THE_PDF_API_URL="http://localhost:8000/querythepdf"
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

The frontend will now be accessible at http://localhost:3000 by default, providing a user interface to interact with the image vector search demo.

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
