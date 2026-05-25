import os
import glob
import pickle
import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------

DATA_FOLDER = "data"
VECTORSTORE_FOLDER = "vectorstore"

FAISS_INDEX_PATH = os.path.join(VECTORSTORE_FOLDER, "faiss_index.bin")
METADATA_PATH = os.path.join(VECTORSTORE_FOLDER, "metadata.pkl")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

print("Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

# -----------------------------
# READ ALL CSV FILES
# -----------------------------

csv_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))

all_chunks = []

print(f"Found {len(csv_files)} CSV files")

for file_path in csv_files:

    try:
        df = pd.read_csv(file_path)

        print(f"\nProcessing: {file_path}")
        print(f"Rows: {len(df)}")

        # Convert every row into text chunk
        for _, row in df.iterrows():

            chunk = ""

            for column in df.columns:
                value = row[column]
                chunk += f"{column}: {value}\n"

            all_chunks.append(chunk)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------

print("\nCreating embeddings...")

embeddings = model.encode(
    all_chunks,
    show_progress_bar=True
)

# Convert to float32
embeddings = embeddings.astype("float32")

# -----------------------------
# CREATE FAISS INDEX
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# -----------------------------
# SAVE INDEX
# -----------------------------

os.makedirs(VECTORSTORE_FOLDER, exist_ok=True)

faiss.write_index(index, FAISS_INDEX_PATH)

# -----------------------------
# SAVE METADATA
# -----------------------------

with open(METADATA_PATH, "wb") as f:
    pickle.dump(all_chunks, f)

# -----------------------------
# DONE
# -----------------------------

print("\n===================================")
print("FAISS index created successfully!")
print(f"Total chunks stored: {len(all_chunks)}")
print(f"Index saved at: {FAISS_INDEX_PATH}")
print(f"Metadata saved at: {METADATA_PATH}")
print("===================================")