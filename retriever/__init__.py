# Retriever package for AI Insight
"""
Retriever Package for AI Insight

This package contains modules for building and querying FAISS indexes
for database schema retrieval using embeddings.

Modules:
- build_index: Script to extract and embed table schemas
- query_index: Function to retrieve relevant tables from the index
"""

from .query_index import retrieve_tables
from .build_index import *

__version__ = "1.0.0"
__author__ = "AI Insight Team"

__all__ = [
    "retrieve_tables"
]
