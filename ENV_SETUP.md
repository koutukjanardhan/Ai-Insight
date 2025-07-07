# Environment Variables Setup

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
   ```

## Environment Variables Reference

### LLM Configuration
- `LLM_API_KEY` - Your LLM provider API key (required)
- `LLM_BASE_URL` - Base URL for LLM API (default: OpenAI)
- `LLM_MODEL` - Model name to use (default: gpt-3.5-turbo)

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

## Security Notes

- Never commit your `.env` file to version control
- The `.env.example` file should only contain example values
- Keep your API keys secure and rotate them regularly
