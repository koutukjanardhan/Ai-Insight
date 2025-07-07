# Retriever Package

This package handles the RAG (Retrieval Augmented Generation) functionality for the AI Insight application. It builds and queries FAISS indexes for database schema information to enable intelligent natural language querying.

## Overview

The retriever works by:
1. **Analyzing your database schema** (tables, columns, relationships)
2. **Creating semantic embeddings** for each schema element
3. **Building a FAISS index** for fast similarity search
4. **Enabling natural language queries** to find relevant tables/columns

**⚠️ Important**: You MUST have a database set up before using the retriever. The system needs actual database schema to analyze and index.

## Files

### `build_index.py`
Script to extract table schemas from your SQLite database and create FAISS embeddings.

**⚠️ Prerequisites:**
- A SQLite database file must exist and be configured in `DATABASE_PATH`
- Database must contain tables with actual schema (empty databases won't work)

**Features:**
- Extracts comprehensive schema information from SQLite databases
- Generates semantic embeddings for tables, columns, and relationships
- Creates FAISS index with metadata for fast similarity search
- Analyzes table structure and column types for better context

**Usage:**
```bash
# Make sure your database is set up first
# Check that DATABASE_PATH in .env points to your database

cd retriever
python build_index.py
```

**What it does:**
1. Connects to your SQLite database using `DATABASE_PATH` from config
2. Extracts all table names and column information
3. Creates text descriptions: "Table: customers | Columns: id, name, email, phone"
4. Generates embeddings using the configured embedding model
5. Stores FAISS index and metadata in `retriever/faiss_index/`

**Output files:**
- `schema.index` - FAISS vector index
- `table_names.pkl` - Table names and schema text mapping

### `query_index.py`
Functions to retrieve relevant tables and columns based on natural language queries.

**Features:**
- Query relevant schema elements using natural language
- Find tables by business concepts
- Discover related columns within tables
- Calculate table similarity scores
- Suggest related tables

**Usage:**
```python
from retriever import retrieve_relevant_tables

# Get relevant tables for a query
context = retrieve_relevant_tables("customer sales data", top_k=5)
print(context['relevant_tables'])
```

### `faiss_index/`
Directory containing the generated FAISS index files:
- `schema_index.faiss` - The FAISS index
- `metadata.pkl` - Metadata for each indexed item
- `embeddings.npy` - Raw embeddings for analysis

## Workflow

### First Time Setup (Required)

1. **Set up your database**:
   ```bash
   # Option A: Use existing database
   cp /path/to/your/database.db ./my_database.db
   
   # Option B: Create sample database
   sqlite3 sample.db "
   CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
   CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
   INSERT INTO customers VALUES (1, 'John Doe', 'john@example.com');
   INSERT INTO orders VALUES (1, 1, 100.50);
   "
   ```

2. **Configure database path**:
   ```bash
   # Update .env file
   DATABASE_PATH=my_database.db  # or sample.db
   ```

3. **Build the vector index**:
   ```bash
   # This step is REQUIRED before using the application
   python retriever/build_index.py
   ```
   
   Expected output:
   ```
   ✅ Vector index built and stored.
   ```

### Normal Usage

1. **Query the index**: Use functions from `query_index.py` to retrieve relevant context
2. **Rebuild when needed**: Re-run `build_index.py` when your database schema changes

### When to Rebuild Index

- When you add/remove tables from your database
- When you change column names or types
- When you switch to a different database
- When you change the embedding model in config

## Integration

The retriever integrates with the main application through:
- `app/rag_retriever.py` - Main RAG client that uses this package
- `app/routes.py` - API endpoints that use retrieval results
- `app/prompts.py` - Templates that format retrieval context

## Configuration

The retriever uses the same configuration as the main app:
- `EMBEDDING_MODEL` - Sentence transformer model for embeddings
- `VECTOR_STORE_PATH` - Where to store FAISS files (falls back to ./faiss_index)
- `TOP_K_RETRIEVAL` - Default number of results to retrieve

## Dependencies

- `sentence-transformers` - For generating embeddings
- `faiss-cpu` - For similarity search
- `numpy` - For array operations
- `pickle` - For metadata serialization

## Performance Notes

- Index building is a one-time operation (unless schema changes)
- Query performance is very fast (~1ms for typical queries)
- Memory usage scales with database size (typically <100MB for most databases)
- Embeddings are normalized for cosine similarity

## Troubleshooting

**"No such file or directory" error when building index:**
```bash
FileNotFoundError: [Errno 2] No such file or directory: 'sakila.db'
```
- **Solution**: Set up your database first (see Workflow section above)
- Check that `DATABASE_PATH` in `.env` points to an existing database file

**"No tables found in database!" error:**
```bash
❌ No tables found in database!
```
- **Solution**: Your database is empty or has no tables
- Create tables in your database or use a different database file
- Verify database isn't corrupted: `sqlite3 your_database.db ".tables"`

**Index files not found when querying:**
- **Solution**: Run `python retriever/build_index.py` first to create the index
- Vector index must be built before the application can work

**Import errors:**
- Ensure the parent app directory is in Python path
- Install all dependencies from requirements.txt: `pip install -r requirements.txt`

**Poor retrieval quality:**
- Try different embedding models in config (`EMBEDDING_MODEL` in `.env`)
- Rebuild index with more sample data in your database
- Adjust query phrasing to be more specific
- Ensure your database has meaningful table and column names

**Vector index appears to be outdated:**
- Delete `retriever/faiss_index/` directory
- Run `python retriever/build_index.py` to rebuild with current database schema
