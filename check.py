#!/usr/bin/env python3
"""
Vector Relation Map & LLM Configuration Checker
This script analyzes and displays:
1. Vector embeddings and their relationships for the database schema stored in the FAISS index
2. LLM configuration and environment variables for diagnostics
"""

import os
import sys
import pickle
import numpy as np
from pathlib import Path

# Add app directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    from app.config import Config
    from app.llm_client import LLMClient
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Please install required packages: pip install faiss-cpu sentence-transformers")
    sys.exit(1)

def print_llm_configuration():
    """Print LLM configuration and environment variables for diagnostics"""
    print("🤖 LLM CONFIGURATION DIAGNOSTICS")
    print("=" * 40)
    
    # Load configuration
    config = Config()
    
    # Display LLM-related environment variables
    print("📋 ENVIRONMENT VARIABLES")
    print("-" * 25)
    
    llm_env_vars = [
        'LLM_API_KEY',
        'LLM_BASE_URL', 
        'LLM_MODEL',
        'MAX_TOKENS',
        'TEMPERATURE',
        'ANTHROPIC_API_KEY',
        'OPENAI_API_KEY'
    ]
    
    for var in llm_env_vars:
        value = os.getenv(var)
        if value:
            if 'API_KEY' in var:
                # Mask API keys for security
                masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                print(f"  {var}: {masked_value}")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: ❌ Not set")
    
    print()
    
    # Display config values
    print("⚙️  CONFIG VALUES")
    print("-" * 18)
    
    try:
        print(f"  LLM API Key: {'✅ Set' if config.LLM_API_KEY else '❌ Not set'}")
        print(f"  LLM Base URL: {config.LLM_BASE_URL}")
        print(f"  LLM Model: {config.LLM_MODEL}")
        print(f"  Max Tokens: {config.MAX_TOKENS}")
        print(f"  Temperature: {config.TEMPERATURE}")
    except AttributeError as e:
        print(f"  ❌ Config attribute error: {e}")
    
    print()
    
    # Test LLM client initialization
    print("🔧 LLM CLIENT TEST")
    print("-" * 18)
    
    try:
        llm_client = LLMClient()
        print("  ✅ LLMClient initialized successfully")
        
        # Check which provider is being used
        if hasattr(llm_client, 'client'):
            client_type = type(llm_client.client).__name__
            print(f"  🏷️  Client Type: {client_type}")
        
        # Test basic configuration
        if hasattr(llm_client, 'model'):
            print(f"  🎯 Active Model: {llm_client.model}")
        
    except Exception as e:
        print(f"  ❌ LLMClient initialization failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()

def load_vector_index():
    """Load the FAISS index and metadata"""
    config = Config()
    index_path = config.VECTOR_STORE_PATH
    
    if not os.path.exists(index_path):
        print(f"❌ Vector store directory not found: {index_path}")
        print("Run 'python retriever/build_index.py' first to create the index.")
        return None, None, None
    
    # Load FAISS index
    index_file = os.path.join(index_path, "schema.index")
    if not os.path.exists(index_file):
        print(f"❌ FAISS index file not found: {index_file}")
        return None, None, None
    
    index = faiss.read_index(index_file)
    
    # Load metadata
    metadata_file = os.path.join(index_path, "table_names.pkl")
    if not os.path.exists(metadata_file):
        print(f"❌ Metadata file not found: {metadata_file}")
        return None, None, None
    
    with open(metadata_file, "rb") as f:
        schema_texts, table_names = pickle.load(f)
    
    return index, schema_texts, table_names

def calculate_similarity_matrix(index, schema_texts, model):
    """Calculate similarity matrix between all schema elements"""
    # Get all vectors from the index
    vectors = index.reconstruct_n(0, index.ntotal)
    
    # Calculate cosine similarity matrix
    # Normalize vectors for cosine similarity
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    normalized_vectors = vectors / norms
    
    # Compute similarity matrix
    similarity_matrix = np.dot(normalized_vectors, normalized_vectors.T)
    
    return similarity_matrix

def print_vector_relation_map():
    """Print the vector relation map"""
    print("🔍 VECTOR RELATION MAP ANALYZER")
    print("=" * 50)
    
    # Load configuration
    config = Config()
    print(f"📊 Database: {config.DATABASE_PATH}")
    print(f"🧠 Embedding Model: {config.EMBEDDING_MODEL}")
    print(f"📁 Vector Store: {config.VECTOR_STORE_PATH}")
    print()
    
    # Load vector index
    print("📥 Loading vector index...")
    index, schema_texts, table_names = load_vector_index()
    
    if index is None:
        return
    
    print(f"✅ Loaded {index.ntotal} vectors")
    print(f"📐 Vector dimension: {index.d}")
    print()
    
    # Load embedding model
    print("🤖 Loading embedding model...")
    model = SentenceTransformer(f"sentence-transformers/{config.EMBEDDING_MODEL}")
    print("✅ Model loaded")
    print()
    
    # Display schema information
    print("📋 DATABASE SCHEMA MAPPING")
    print("-" * 30)
    for i, (table_name, schema_text) in enumerate(zip(table_names, schema_texts)):
        print(f"{i+1:2d}. {table_name}")
        print(f"    📝 {schema_text}")
        print()
    
    # Calculate similarity matrix
    print("🧮 CALCULATING VECTOR SIMILARITIES")
    print("-" * 35)
    similarity_matrix = calculate_similarity_matrix(index, schema_texts, model)
    
    # Display similarity relationships
    print("🔗 TABLE RELATIONSHIPS (Cosine Similarity)")
    print("-" * 45)
    
    # Find most similar pairs
    similarities = []
    for i in range(len(table_names)):
        for j in range(i+1, len(table_names)):
            sim = similarity_matrix[i][j]
            similarities.append((i, j, sim, table_names[i], table_names[j]))
    
    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    print("Top 10 Most Similar Table Pairs:")
    for i, (idx1, idx2, sim, table1, table2) in enumerate(similarities[:10]):
        print(f"{i+1:2d}. {table1} ↔ {table2}")
        print(f"    📊 Similarity: {sim:.4f}")
        print()
    
    # Display similarity matrix (heatmap style)
    print("🌡️  SIMILARITY HEATMAP")
    print("-" * 25)
    print("     ", end="")
    for i, table in enumerate(table_names):
        print(f"{i+1:3d}", end="")
    print()
    
    for i, table in enumerate(table_names):
        print(f"{i+1:2d}. ", end="")
        for j in range(len(table_names)):
            sim = similarity_matrix[i][j]
            if i == j:
                print(" ██", end="")  # Self-similarity
            elif sim > 0.8:
                print(" ▓▓", end="")  # High similarity
            elif sim > 0.6:
                print(" ▒▒", end="")  # Medium similarity
            elif sim > 0.4:
                print(" ░░", end="")  # Low similarity
            else:
                print(" ··", end="")  # Very low similarity
        print(f" {table}")
    
    print()
    print("Legend: ██ Self  ▓▓ High(>0.8)  ▒▒ Med(>0.6)  ░░ Low(>0.4)  ·· VeryLow")
    print()
    
    # Test query similarity
    print("🔍 QUERY SIMILARITY TEST")
    print("-" * 25)
    test_queries = [
        "customer information",
        "sales data",
        "product details",
        "order history",
        "payment records"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        query_vector = model.encode([query])
        D, I = index.search(query_vector, min(3, len(table_names)))
        
        print("  Top matches:")
        for j, (distance, idx) in enumerate(zip(D[0], I[0])):
            similarity = 1 / (1 + distance)  # Convert distance to similarity
            print(f"    {j+1}. {table_names[idx]} (similarity: {similarity:.4f})")
        print()
    
    print("✅ Vector relation map analysis complete!")

if __name__ == "__main__":
    try:
        # Print LLM configuration first
        print_llm_configuration()
        print("\n" + "="*70 + "\n")
        
        # Then print vector relation map
        print_vector_relation_map()
    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
