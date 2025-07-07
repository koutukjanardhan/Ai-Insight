import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    def generate_sql(self, prompt: str) -> str:
        """
        Call the custom LLM to generate SQL based on the provided prompt.
        """
        # Handle API key format - if it already starts with "Token", use as-is
        auth_header = self.api_key if self.api_key.startswith("Token ") else f"Token {self.api_key}"
        
        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful SQL assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(
                f"{self.base_url}/llm/chat/completions",
                json=payload,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"❌ LLM API Error: {e}")
            return ""
