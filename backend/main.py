from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from ask_llm import retrieval
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

#origins = os.getenv("ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.get("/")
async def root():
    return {"status": "OK"}

# AskLeafy endpoint
@app.post("/askTheLlm")
async def ask_llm(request: Request):
    data = await request.json()
    question = data.get("question")
    similar_docs, llm_output = retrieval(question)
    return {"question": question, "result": llm_output, "similar_docs": similar_docs}
