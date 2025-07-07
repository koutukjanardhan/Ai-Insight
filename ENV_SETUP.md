# Environment Variables Setup - Vector-Enhanced AI Database Query System

## Quick Start

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your actual API keys and configuration:
   ```bash
   # Required: Set your LLM API key
   LLM_API_KEY=your_actual_api_key_here
   
   # Optional: Customize other settings
   LLM_MODEL=gpt-3.5-turbo
   PORT=8000
   DEBUG=True
   
   # Vector Configuration (Critical for AI Features)
   VECTOR_STORE_PATH=retriever/faiss_index
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   TOP_K_RETRIEVAL=5
   ```

## Environment Variables Reference

### 🔬 Vector Embeddings Configuration
- `VECTOR_STORE_PATH` - Path to FAISS vector index (default: retriever/faiss_index)
- `EMBEDDING_MODEL` - Sentence transformer model for vectorization (default: all-MiniLM-L6-v2)  
- `TOP_K_RETRIEVAL` - Number of similar vectors to retrieve for context (default: 5)

### 🤖 LLM Configuration
- `LLM_API_KEY` - Your LLM provider API key (required)
- `LLM_BASE_URL` - Base URL for LLM API (default: OpenAI)
- `LLM_MODEL` - Model name to use (default: gpt-3.5-turbo)
- `MAX_TOKENS` - Maximum tokens for LLM response (default: 500)
- `TEMPERATURE` - LLM creativity/randomness (default: 0.1)

### Database Configuration
- `DATABASE_PATH` - Path to SQLite database file (default: sakila.db)

### Application Configuration
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Enable debug mode (default: True)

## Supported LLM Providers

### OpenAI (Default)
```env
LLM_API_KEY=sk-your-openai-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
```

### Azure OpenAI
```env
LLM_API_KEY=your-azure-key
LLM_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
LLM_MODEL=gpt-35-turbo
```

### Local LLM (Ollama)
```env
LLM_API_KEY=not-needed-for-local
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama2
```

### Anthropic Claude
```env
LLM_API_KEY=your-anthropic-key
LLM_BASE_URL=https://api.anthropic.com/v1
LLM_MODEL=claude-3-sonnet-20240229
```

## 🚀 Staging Environment Configuration

### Vector Index Locations for Different Environments

#### Development Environment
```env
VECTOR_STORE_PATH=retriever/faiss_index
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K_RETRIEVAL=5
DEBUG=True
```

#### Staging Environment
```env
VECTOR_STORE_PATH=retriever/retriever/faiss_index  # Alternative staging location
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K_RETRIEVAL=3                                  # Faster for staging tests
DEBUG=False
```

#### Production Environment
```env
VECTOR_STORE_PATH=/opt/ai-insight/vector_store      # Production path
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K_RETRIEVAL=5
DEBUG=False
MAX_TOKENS=1000                                     # Higher limits for production
TEMPERATURE=0.05                                    # More deterministic for production
```

### 🔬 Vector System Environment Variables

- `VECTOR_STORE_PATH` - **Critical**: Location of FAISS vector index files
- `EMBEDDING_MODEL` - Sentence transformer model (384-dimensional embeddings)
- `TOP_K_RETRIEVAL` - Number of semantically similar elements to retrieve
- `BUILD_INDEX_ON_STARTUP` - Auto-rebuild vector index if missing (default: False)
- `VECTOR_CACHE_SIZE` - Number of vectors to cache in memory (default: 1000)

### 🎯 Performance Tuning by Environment

| Environment | TOP_K_RETRIEVAL | MAX_TOKENS | TEMPERATURE | Purpose |
|-------------|-----------------|------------|-------------|---------|
| Development | 5 | 500 | 0.1 | Full context, debugging |
| Staging | 3 | 300 | 0.05 | Fast testing, validation |
| Production | 5 | 1000 | 0.02 | Optimal accuracy, deterministic |

## Security Notes

- Never commit your `.env` file to version control
- The `.env.example` file should only contain example values
- Keep your API keys secure and rotate them regularly
