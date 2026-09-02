# AGENTS.md

Guidance for AI coding agents working in this repository.

This is a RAG demo for insurance claims. A FastAPI backend (`backend/`) embeds a
question with Cohere via AWS Bedrock, runs Atlas Vector Search over the
`claims_final` collection, and asks a Bedrock Claude Haiku model to answer grounded
in the retrieved claims. A Next.js frontend (`frontend/`) calls the backend's single
`POST /askTheLlm` endpoint and renders the answer alongside the source claims.

## Build and test commands

```bash
# Backend (from backend/)
poetry install                                          # install dependencies
poetry run uvicorn main:app --host 0.0.0.0 --port 8000   # start the API on :8000

# Frontend (from frontend/)
npm install     # install dependencies
npm run dev      # dev server on :8080 (next dev -p 8080)
npm run build    # production build
npm run start     # serve the production build on :8080
```

Supporting scripts (from `backend/`, requires Atlas — see constraints below):

```bash
poetry run python embeddingsInitializer.py              # backfills claimDescriptionEmbeddingCohere on every seeded document
poetry run python scripts/create_vector_search_index.py  # idempotently creates vector_index_claim_description_cohere
```

**There is no automated test suite in this repository.** Neither `backend/pyproject.toml`
nor `frontend/package.json` defines a `test` command. To verify a change, run the
backend and frontend dev servers and exercise `POST /askTheLlm` (directly or through the
UI) with a real question. Do not claim tests pass — there are none.

Smoke check after a change:

1. Seed `claims_final` (see README) and run the two supporting scripts above.
2. Start the backend (`poetry run uvicorn main:app --host 0.0.0.0 --port 8000`).
3. `curl -X POST http://localhost:8000/askTheLlm -H "Content-Type: application/json" -d '{"question": "<a claims-related question>"}'`
4. Confirm the response has non-empty `result` and `similar_docs` with 3 entries.

## Project structure

```
backend/
  main.py                      FastAPI app; defines POST /askTheLlm
  ask_llm.py                   vector_search() + ask_llm() + retrieval() — the RAG pipeline
  bedrock_client.py            boto3 Bedrock client construction (region, profile, assumed role)
  embeddingsInitializer.py     one-off script: backfills claimDescriptionEmbeddingCohere
  scripts/create_vector_search_index.py   one-off script: creates the Atlas vector index
  pyproject.toml               Poetry deps (fastapi, pymongo, langchain-mongodb, langchain-aws)
frontend/
  app/                         Next.js app router pages
  components/                  UI components (LeafyGreen UI)
  package.json                 scripts (dev/build/start), dependencies
data/
  demo_rag_insurance.claims.json   seed dataset for mongoimport
EDD.md                          MongoDB data model reference — read before touching claims_final
README.md                       product overview and setup walkthrough
```

Notable files:

- `backend/ask_llm.py` — the entire RAG pipeline: builds `MongoDBAtlasVectorSearch`
  over `claimDescriptionEmbeddingCohere`, strips other embedding fields from results,
  and calls the Haiku model with the retrieved claims as context.
- `backend/main.py` — the only HTTP surface; one route, `POST /askTheLlm`.
- `backend/scripts/create_vector_search_index.py` — must be run against Atlas after
  seeding; there is no local-MongoDB equivalent of `create_search_index`.

## API overview

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | health check, returns `{"status": "OK"}` |
| POST | `/askTheLlm` | body `{"question": string}`; runs vector search + LLM, returns `{"question", "result", "similar_docs"}` |

## Environment variables and configuration

| Name | Required | Example | Description |
| --- | --- | --- | --- |
| `MONGODB_URI` | Yes (backend) | `mongodb+srv://...` | Atlas connection string used by `main.py`/`ask_llm.py`/`embeddingsInitializer.py`/`create_vector_search_index.py` |
| `AWS_KEY_REGION` | Yes (backend) | `us-east-1` | region passed to `BedrockClient` for both embeddings and the Haiku model |
| `AWS_PROFILE` | No | `default` | named AWS CLI profile picked up by `boto3.Session` in `bedrock_client.py` |
| `AWS_REGION` / `AWS_DEFAULT_REGION` | No | `us-east-1` | fallback region if `AWS_KEY_REGION` is unset |
| `BEDROCK_MODEL_HAIKU` | No | `us.anthropic.claude-haiku-4-5-20251001-v1:0` | overrides the Bedrock LLM model id used in `ask_llm.py` |
| `BEDROCK_MODEL_COHERE_EMBED` | No | `cohere.embed-english-v3` | overrides the Bedrock embedding model id used for both the initializer script and query-time embedding |
| `NEXT_PUBLIC_ASK_LEAFY_API_URL` | Yes (frontend) | `http://localhost:8000/askTheLlm` | full URL the frontend POSTs questions to |

Constraints worth knowing before you debug a failure:

- Vector index creation is Atlas-only. `scripts/create_vector_search_index.py` calls
  `collection.create_search_index`, which does not exist on a local/self-hosted
  `mongod` — against anything but Atlas, seeding succeeds and index creation fails.
- Retrieval depends on `embeddingsInitializer.py` having already run. Freshly seeded
  documents (via `mongoimport`) don't yet carry `claimDescriptionEmbeddingCohere`, so
  vector search returns nothing until the initializer backfills it.
- The frontend and backend ports are fixed by convention, not enforced: backend on
  `8000` (per the `uvicorn` command in the README), frontend on `8080` (baked into
  `frontend/package.json`'s `dev`/`start` scripts). `NEXT_PUBLIC_ASK_LEAFY_API_URL`
  must point at the backend's actual host:port including the `/askTheLlm` path.

## MongoDB Skills

Use the official MongoDB agent skills from https://github.com/mongodb/agent-skills
whenever the task is MongoDB-specific and a matching skill exists.

## When To Use EDD.md

Use [EDD.md](./EDD.md) as the source of truth for the MongoDB data model in this repository.

Consult [EDD.md](./EDD.md) before making changes that touch:

- MongoDB collections, document structure, or field names
- FastAPI routes that read or write database records
- Validation, form fields, API payloads, or UI that depend on persisted data
- Schema documentation, Mermaid diagrams, or entity modeling discussions
