import sqlite3
import os
from .config import Config

def run_query(sql: str):
    """
    Executes the given SQL on the SQLite DB and returns column names + rows.
    If there's an error, returns ([], error_message).
    """
    config = Config()
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return columns, rows
    except Exception as e:
        return [], f"SQL Error: {e}"