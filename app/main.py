from fastapi import FastAPI
import sys
import os

# Add parent directory to path for imports when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.router import router

app = FastAPI(title="AI SQL Agent", version="1.0")

# Include the /ask endpoint
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "AI Insight API is running!"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", "8001"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
