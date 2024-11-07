from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from ask_llm import retrieval


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.post("/askTheLlm")
async def ask_llm(request: Request):
    data = await request.json()
    question = data.get("question")
    similar_docs, llm_output = retrieval(question)
    return {"question": question, "result": llm_output, "similar_docs": similar_docs}

    
