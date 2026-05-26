import os
import pickle
import faiss
import numpy as np

from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

import uuid
from datetime import datetime

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# -----------------------------------
# PATHS
# -----------------------------------

FAISS_INDEX_PATH = "vectorstore/faiss_index.bin"
METADATA_PATH = "vectorstore/metadata.pkl"

# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------
# LOAD FAISS INDEX
# -----------------------------------

print("Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX_PATH)

# -----------------------------------
# LOAD METADATA
# -----------------------------------

print("Loading metadata...")
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

# -----------------------------------
# LOAD GROQ CLIENT
# -----------------------------------

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------------
# MAIN FUNCTION
# -----------------------------------

def analyze_incident(user_query):

    # -----------------------------------
    # STEP 1 — CREATE QUERY EMBEDDING
    # -----------------------------------

    query_embedding = embedding_model.encode([user_query])

    query_embedding = np.array(query_embedding).astype("float32")

    # -----------------------------------
    # STEP 2 — SEARCH FAISS
    # -----------------------------------

    top_k = 5

    distances, indices = index.search(query_embedding, top_k)

    # -----------------------------------
    # STEP 3 — RETRIEVE CONTEXT
    # -----------------------------------

    retrieved_context = ""

    for idx in indices[0]:

        if idx < len(metadata):

            retrieved_context += metadata[idx]
            retrieved_context += "\n\n----------------------\n\n"

    # -----------------------------------
    # STEP 4 — CREATE PROMPT
    # -----------------------------------

    prompt = f"""
You are an enterprise operations RCA assistant.

Your role:
- Analyze operational incidents
- Predict probable root causes
- Identify affected systems
- Suggest remediation steps
- Correlate historical incidents
- Use the enterprise operational knowledge provided below

Enterprise Knowledge Base:
{retrieved_context}

Current Incident:
{user_query}

Provide response in this format:

1. Probable Root Cause
2. Incident Severity
3. Affected Systems
4. Similar Historical Incidents
5. Recommended Remediation
6. Operational Summary
"""

    # -----------------------------------
    # STEP 5 — CALL GROQ
    # -----------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent enterprise operations copilot."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    # -----------------------------------
    # STEP 6 — RETURN RESPONSE
    # -----------------------------------

    return response.choices[0].message.content
# -----------------------------------
# ADD NEW INCIDENT TO KNOWLEDGE BASE
# -----------------------------------


# -----------------------------------
# ADD NEW INCIDENT TO KNOWLEDGE BASE
# -----------------------------------

def add_incident_to_knowledgebase(user_query, ai_response):

    # -----------------------------------
    # GENERATE INCIDENT ID
    # -----------------------------------

    incident_id = f"INC-{str(uuid.uuid4())[:8].upper()}"

    # -----------------------------------
    # TIMESTAMP
    # -----------------------------------

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -----------------------------------
    # CREATE NEW CHUNK
    # -----------------------------------

    new_chunk = f"""
INCIDENT ID: {incident_id}

TIMESTAMP: {timestamp}

NEW INCIDENT REPORTED

Incident Details:
{user_query}

AI RCA Analysis:
{ai_response}
"""

    # -----------------------------------
    # CREATE EMBEDDING
    # -----------------------------------

    new_embedding = embedding_model.encode([new_chunk])

    new_embedding = np.array(new_embedding).astype("float32")

    # -----------------------------------
    # ADD TO FAISS
    # -----------------------------------

    index.add(new_embedding)

    # -----------------------------------
    # ADD TO METADATA
    # -----------------------------------

    metadata.append(new_chunk)

    # -----------------------------------
    # SAVE UPDATED INDEX
    # -----------------------------------

    faiss.write_index(index, FAISS_INDEX_PATH)

    # -----------------------------------
    # SAVE UPDATED METADATA
    # -----------------------------------

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"New incident stored: {incident_id}")

    return incident_id
