# Configuration settings for API keys, paths, and other settings
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the AI Insight application"""
    
    # LLM Configuration (Updated to use generic LLM settings)
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # Legacy OpenAI support (for backward compatibility)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "sakila.db")
    
    # Vector Store Configuration
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "retriever/faiss_index")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # RAG Configuration
    TOP_K_RETRIEVAL: int = int(os.getenv("TOP_K_RETRIEVAL", "5"))
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # LLM Configuration
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "500"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    def __init__(self):
        """Initialize configuration and validate required settings"""
        self._validate_config()
        self._ensure_paths_exist()
    
    def _validate_config(self):
        """Validate required configuration settings"""
        # Only require API key for LLM operations, not for retriever tools
        if not self.OPENAI_API_KEY and not self.LLM_API_KEY:
            print("Warning: No LLM API key found. LLM operations will not work.")
            print("Set LLM_API_KEY or OPENAI_API_KEY environment variable for full functionality.")
    
    def _ensure_paths_exist(self):
        """Ensure required directories exist"""
        # Create vector store directory if it doesn't exist
        Path(self.VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
        
        # Check if SQLite file exists (create warning if not)
        if not os.path.exists(self.DATABASE_PATH):
            print(f"Warning: SQLite database file not found at {self.DATABASE_PATH}")
            print("Please ensure the database file exists or update the DATABASE_PATH configuration")
    
    @classmethod
    def from_env_file(cls, env_file: str = ".env"):
        """Load configuration from .env file"""
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        return cls()
    
    def get_database_url(self) -> str:
        """Get the database connection URL"""
        return f"sqlite:///{self.DATABASE_PATH}"
    
    def get_vector_store_config(self) -> dict:
        """Get vector store configuration"""
        return {
            "path": self.VECTOR_STORE_PATH,
            "embedding_model": self.EMBEDDING_MODEL,
            "top_k": self.TOP_K_RETRIEVAL
        }
    
    def get_llm_config(self) -> dict:
        """Get LLM configuration"""
        return {
            "model_name": self.MODEL_NAME,
            "max_tokens": self.MAX_TOKENS,
            "temperature": self.TEMPERATURE,
            "api_key": self.OPENAI_API_KEY
        }
