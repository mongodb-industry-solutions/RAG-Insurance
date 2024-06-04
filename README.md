# Insurance RAG demo

Create a file named '.env' and store your OpenAI API key and MongoDB connection string in it, follow this format:

```bash
OPENAI_API_KEY=<your key>
MONGO_URI="mongodb+srv://<usr>:<pswd>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
```
In MongoDB Atlas create a databse called "demo_rag_insurance" and a collection called "claims_final", import the dataset "demo_rag_insurance.claims.json" into the collection. You have to create two Vector Search Indexes, one for "claimDescriptionEmbedding" called "vector_index_claim_description" and one for "photoEmbedding" called "default":

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "claimDescriptionEmbedding",
      "numDimensions": 350,
      "similarity": "cosine"
    }
  ]
}
```
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "photoEmbedding",
      "numDimensions": 1000,
      "similarity": "cosine"
    }
  ]
}
```
run

``` bash  
pip install -r requirements.txt
```

and then launch the backend

```bash
python3 -m uvicorn main:app --reload
```
move to the frontend folder and run the frontend

```bash
npm install
npm start
```

## Docker Setup Instructions

To run the application using Docker, follow these setup steps:

### Configure Environment Variables

First, update the docker-compose.yml file with your OpenAI API Key and MongoDB Atlas URI. Find the environment section and add your credentials as shown below:
```
environment:
      - OPENAI_API_KEY=your_openai_api_key_here
      - MONGO_URI=your_mongodb_atlas_uri_here
```
### Build the Application

To build the Docker images and start the services, run the following command:
```
make build
```

###  Stopping the Application

To stop all running services, use the command:
```
make stop
````

### Cleaning Up

To remove all images and containers associated with the application, execute:
```
make clean
```


