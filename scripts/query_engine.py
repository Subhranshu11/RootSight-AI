import os
import pickle
import faiss
import numpy as np
import uuid

from datetime import datetime

import streamlit as st

from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# -----------------------------------
# VALID ENTERPRISE KEYWORDS
# -----------------------------------

VALID_ENTERPRISE_KEYWORDS = [
    "incident",
    "scheduler",
    "deployment",
    "etl",
    "dashboard",
    "report",
    "failure",
    "job",
    "refresh",
    "service",
    "server",
    "rca",
    "workflow",
    "database",
    "latency",
    "timeout",
    "ticket",
    "pipeline",
    "application",
    "analytics",
    "data",
    "monitoring",
    "batch",
    "refresh failure",
    "operational",
    "production",
    "alert"
]

# -----------------------------------
# ENTERPRISE QUERY VALIDATION
# -----------------------------------

def is_enterprise_query(user_query):

    user_query = user_query.lower()

    for keyword in VALID_ENTERPRISE_KEYWORDS:

        if keyword in user_query:
            return True

    return False

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

try:

    # Streamlit Cloud
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except:

    # Local Development
    GROQ_API_KEY = "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"

# -----------------------------------
# PATHS
# -----------------------------------

FAISS_INDEX_PATH = "vectorstore/faiss_index.bin"
METADATA_PATH = "vectorstore/metadata.pkl"

# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------------
# LOAD FAISS INDEX
# -----------------------------------

print("Loading FAISS index...")

index = faiss.read_index(
    FAISS_INDEX_PATH
)

# -----------------------------------
# LOAD METADATA
# -----------------------------------

print("Loading metadata...")

with open(METADATA_PATH, "rb") as f:

    metadata = pickle.load(f)

# -----------------------------------
# LOAD GROQ CLIENT
# -----------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)

# -----------------------------------
# MAIN INCIDENT ANALYSIS FUNCTION
# -----------------------------------

def analyze_incident(
    user_query,
    return_context=False
):

    # -----------------------------------
    # ENTERPRISE SCOPE VALIDATION
    # -----------------------------------

    if not is_enterprise_query(user_query):

        scope_message = """
## Scope Restriction Notice

The requested query is outside the scope of the current enterprise operational knowledge base.

This AI assistant is currently limited to:
- Operational incidents
- Scheduler failures
- ETL disruptions
- Deployment issues
- Dashboard/reporting failures
- Enterprise RCA analysis
- Production support operations

Please submit an enterprise operational incident or reporting-related issue.
"""

        if return_context:

            return {
                "response": scope_message,
                "context": []
            }

        return scope_message

    # -----------------------------------
    # STEP 1 — CREATE QUERY EMBEDDING
    # -----------------------------------

    query_embedding = embedding_model.encode(
        [user_query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    # -----------------------------------
    # STEP 2 — SEARCH FAISS
    # -----------------------------------

    top_k = 5

    _, indices = index.search(
        query_embedding,
        top_k
    )

    # -----------------------------------
    # STEP 3 — RETRIEVE CONTEXT
    # -----------------------------------

    retrieved_context = ""

    retrieved_chunks = []

    for idx in indices[0]:

        if idx < len(metadata):

            chunk = metadata[idx]

            retrieved_chunks.append(chunk)

            retrieved_context += chunk
            retrieved_context += "\n\n----------------------\n\n"

    # -----------------------------------
    # STEP 4 — CREATE PROMPT
    # -----------------------------------

    prompt = f"""
You are an enterprise operational intelligence assistant specialized in reporting and analytics environments.

Your responsibility is to provide concise, operationally scoped, enterprise-grade incident analysis.

STRICT RULES:
- Do NOT generate generic AI explanations
- Do NOT speculate outside provided context
- Keep response concise and operational
- Focus only on enterprise reporting operations
- Avoid unnecessary technical jargon
- Keep each section short and actionable
- Use bullet points wherever appropriate
- Severity must be ONLY:
  Critical / High / Medium / Low
- If information is unavailable in enterprise context, clearly mention it
- Never answer outside enterprise operational scope

Your role:
- Analyze operational incidents
- Predict probable root causes
- Identify affected systems
- Suggest remediation steps
- Correlate historical incidents
- Use the enterprise operational knowledge provided below

Enterprise Operational Knowledge Base:
{retrieved_context}

Current Incident:
{user_query}

Provide response EXACTLY in this format:

## Incident Summary
(2-3 concise lines)

## Probable Root Cause
- Point 1
- Point 2

## Severity
Critical / High / Medium / Low

## Affected Components
- Component 1
- Component 2

## Recommended Remediation
- Action 1
- Action 2
- Action 3

## Preventive Recommendation
- Recommendation 1
- Recommendation 2

## Operational Insight
(1 concise enterprise operational observation)
"""

    # -----------------------------------
    # STEP 5 — CALL GROQ
    # -----------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are an enterprise operational intelligence copilot.

You ONLY answer enterprise operational incident queries.

Never behave like a generic chatbot.

Never provide unrelated information.

Keep all responses concise, enterprise-focused, and operationally scoped.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    # -----------------------------------
    # STEP 6 — RETURN RESPONSE
    # -----------------------------------

    final_response = response.choices[0].message.content

    if return_context:

        return {
            "response": final_response,
            "context": retrieved_chunks
        }

    return final_response

# -----------------------------------
# ADD NEW INCIDENT TO KNOWLEDGE BASE
# -----------------------------------

def add_incident_to_knowledgebase(
    user_query,
    ai_response
):

    # -----------------------------------
    # GENERATE INCIDENT ID
    # -----------------------------------

    incident_id = f"INC-{str(uuid.uuid4())[:8].upper()}"

    # -----------------------------------
    # TIMESTAMP
    # -----------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # -----------------------------------
    # CREATE INCIDENT CHUNK
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

    new_embedding = embedding_model.encode(
        [new_chunk]
    )

    new_embedding = np.array(
        new_embedding
    ).astype("float32")

    # -----------------------------------
    # ADD TO FAISS INDEX
    # -----------------------------------

    index.add(new_embedding)

    # -----------------------------------
    # ADD TO METADATA
    # -----------------------------------

    metadata.append(new_chunk)

    # -----------------------------------
    # SAVE UPDATED FAISS INDEX
    # -----------------------------------

    faiss.write_index(
        index,
        FAISS_INDEX_PATH
    )

    # -----------------------------------
    # SAVE UPDATED METADATA
    # -----------------------------------

    with open(METADATA_PATH, "wb") as f:

        pickle.dump(metadata, f)

    print(f"New incident stored: {incident_id}")

    return incident_id
