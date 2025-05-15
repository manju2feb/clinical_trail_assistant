from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import requests
import math
import os

# ========== Configuration ==========
GROQ_API_KEY = "...........use your gok api key"
GROQ_MODEL = "llama3-8b-8192"  # or use "mixtral-8x7b-32768"
#VECTORSTORE_PATH = "../vectorstore"

# ========== Setup ==========
app = FastAPI()
#embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#vectorstore = FAISS.load_local(VECTORSTORE_PATH, embedding_model)
# vectorstore = FAISS.load_local(
#     VECTORSTORE_PATH,
#     embedding_model,
#     allow_dangerous_deserialization=True  
# )
# Use absolute path to avoid runtime errors
VECTORSTORE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../vectorstore"))

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

# ========== Input Schema ==========
# class Query(BaseModel):
#     question: str
class Query(BaseModel):
    question: str
    filters: dict = {}  # Example: {"Phase": "Phase 3", "LocationCountry": "United States"}



# ========== Helper Function ==========
def query_groq_api(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a clinical trial assistant that answers user queries using trial information."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def clean_metadata(meta):
    return {k: ("" if (v is None or isinstance(v, float) and math.isnan(v)) else v) for k, v in meta.items()}

# ========== Endpoint ==========
@app.post("/ask")
async def ask_question(query: Query):
    
    retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": query.filters  # metadata-based filtering
    }
    )
    docs = retriever.get_relevant_documents(query.question)


    #docs = vectorstore.similarity_search(query.question, k=3)

    # Combine relevant info as context
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Use the following clinical trial context to answer the user's question:\n\n{context}\n\nQuestion: {query.question}"

    try:
        answer = query_groq_api(prompt)

        return {
            "answer": answer,
            "sources": [clean_metadata(doc.metadata) for doc in docs]
        }
    except Exception as e:
        return {"error": str(e)}

