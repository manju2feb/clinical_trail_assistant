## Clinical Trial Assistant – AI Chatbot for Real Medical Trials
⚡ Powered by Groq | RAG with FAISS | FastAPI + Streamlit | Built from real ClinicalTrials.gov data

## What it is:
A fast, free, and intelligent chatbot that helps users explore real clinical trial data using natural language. Ask questions like:

"What are the Phase 3 trials for breast cancer in the US?"

"Which COVID-19 trials are sponsored by Pfizer?"

Behind the scenes, the app uses:

* FAISS for fast similarity search

* LangChain for retrieval & metadata filtering

* Groq API to generate answers with ultra-fast LLMs (LLaMA3, Mixtral)

* Streamlit for a chat-style UI

* FastAPI as the backend for semantic Q&A

## Tech Stack

| Component         | Tool                     |
|------------------|--------------------------|
| LLM Inference | [Groq API](https://console.groq.com) |
|  RAG Engine     | [FAISS](https://github.com/facebookresearch/faiss) + [LangChain](https://www.langchain.com/) |
| ector Store   | FAISS (saved locally in `vectorstore/`) |
| Backend        | FastAPI (`/ask` endpoint) |
| Frontend       | Streamlit (`chat_ui.py`) |
| Data Source    | [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api) |
| Deployment     | Render (Free Tier)       |

##  Use Cases

Ask questions like:
- *“What are the Phase 3 cancer trials in the United States?”*
- *“Which clinical trials are sponsored by Pfizer?”*
- *“Are there any ongoing COVID-19 vaccine trials in India?”*

# Try it yourself
git clone 
cd clinical_trail_assistant
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run streamlit_app/chat_ui.py

