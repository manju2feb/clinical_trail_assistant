# scripts/index_trials.py

import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

# Step 1: Load trial data
df = pd.read_csv("../data/trials.csv")
print(f"Loaded {len(df)} trials.")

# Step 2: Convert rows to LangChain Documents
documents = []
for _, row in df.iterrows():
    metadata = {
        "NCTId": row["NCTId"],
        "Phase": row["Phase"],
        "Sponsor": row["Sponsor"]
    }

    content = f"""Title: {row['Title']}
Condition: {row['Condition']}
Phase: {row['Phase']}
Location: {row['LocationCountry']}
Sponsor: {row['Sponsor']}"""

    documents.append(Document(page_content=content, metadata=metadata))

# Step 3: Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4: Store in ChromaDB
persist_dir = "../vectorstore"
if not os.path.exists(persist_dir):
    os.makedirs(persist_dir)

# db = Chroma.from_documents(documents, embedding_model, persist_directory=persist_dir)
# db.persist()
db = FAISS.from_documents(documents, embedding_model)
db.save_local("../vectorstore")

print("FAISS vector store created and saved to: ../vectorstore")

