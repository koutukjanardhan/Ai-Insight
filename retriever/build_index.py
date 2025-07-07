import sqlite3
import faiss
import os
import pickle
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from app.config import Config

# Initialize configuration
config = Config()

DB_PATH = config.DATABASE_PATH
INDEX_PATH = config.VECTOR_STORE_PATH
MODEL_NAME = f"sentence-transformers/{config.EMBEDDING_MODEL}"

os.makedirs(INDEX_PATH, exist_ok=True)

# Step 1: Connect and extract table schemas
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

schema_texts = []
table_names = []

for table in tables:
    cursor.execute(f"PRAGMA table_info({table});")
    cols = [row[1] for row in cursor.fetchall()]
    schema_str = f"Table: {table} | Columns: {', '.join(cols)}"
    schema_texts.append(schema_str)
    table_names.append(table)

conn.close()

# Step 2: Embed using sentence-transformer
model = SentenceTransformer(MODEL_NAME)
embeddings = model.encode(schema_texts, convert_to_numpy=True)

# Step 3: Store in FAISS
if len(schema_texts) == 0:
    print("❌ No tables found in database!")
    exit(1)

if embeddings.ndim == 1:
    # If only one schema, reshape to 2D
    embeddings = embeddings.reshape(1, -1)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, os.path.join(INDEX_PATH, "schema.index"))

# Also save metadata
with open(os.path.join(INDEX_PATH, "table_names.pkl"), "wb") as f:
    pickle.dump((schema_texts, table_names), f)

print("✅ Vector index built and stored.")
