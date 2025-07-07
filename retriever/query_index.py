import faiss
import pickle
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from app.config import Config

# Initialize configuration
config = Config()

INDEX_PATH = config.VECTOR_STORE_PATH
MODEL_NAME = f"sentence-transformers/{config.EMBEDDING_MODEL}"

def retrieve_tables(query, top_k=None):
    if top_k is None:
        top_k = config.TOP_K_RETRIEVAL
        
    # Load index and metadata
    index = faiss.read_index(f"{INDEX_PATH}/schema.index")
    with open(f"{INDEX_PATH}/table_names.pkl", "rb") as f:
        schema_texts, table_names = pickle.load(f)

    # Embed query
    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([query])

    # Search
    D, I = index.search(query_vec, top_k)
    matches = [(table_names[i], schema_texts[i]) for i in I[0]]
    return matches
