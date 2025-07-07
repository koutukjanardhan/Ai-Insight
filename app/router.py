from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.llm_client import LLMClient
from app.prompts import build_prompt
from app.sqlite_client import run_query
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from retriever.query_index import retrieve_tables

router = APIRouter()

# Request body model
class AskRequest(BaseModel):
    question: str

# Response model
class AskResponse(BaseModel):
    sql: str
    columns: list
    rows: list

# FastAPI route
@router.post("/ask", response_model=AskResponse)
def ask_question(req: AskRequest):
    user_question = req.question.strip()

    if not user_question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Step 1: Retrieve relevant table schemas from FAISS
    retrieved = retrieve_tables(user_question)
    if not retrieved:
        raise HTTPException(status_code=404, detail="No relevant tables found.")

    # Step 2: Build LLM prompt
    prompt = build_prompt(user_question, retrieved)

    # Step 3: Call LLM
    llm = LLMClient()
    raw_sql = llm.generate_sql(prompt)

    # Optional: extract SQL cleanly
    from app.utils import extract_sql_from_llm_response
    sql = extract_sql_from_llm_response(raw_sql)
    print(f"Generated SQL: {sql}")

    # Step 4: Run SQL on SQLite
    columns, rows_or_error = run_query(sql)
    if isinstance(rows_or_error, str):  # error message
        raise HTTPException(status_code=500, detail=rows_or_error)

    return AskResponse(sql=sql, columns=columns, rows=rows_or_error)
