# Request and response schemas using Pydantic
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    """Request model for natural language questions"""
    question: str
    
class QueryResponse(BaseModel):
    """Response model for query results"""
    question: str
    sql_query: str
    results: List[Dict[str, Any]]
    success: bool
    error_message: Optional[str] = None
    execution_time: Optional[float] = None

class TableInfo(BaseModel):
    """Model for table metadata"""
    table_name: str
    columns: List[str]
    description: Optional[str] = None

class SchemaInfo(BaseModel):
    """Model for database schema information"""
    tables: List[TableInfo]
    total_tables: int
