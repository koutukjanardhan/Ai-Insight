from typing import List, Tuple

# 🔧 This is your system instruction to guide the LLM
SYSTEM_INSTRUCTION = "You are a SQL lite assistant. Given the following table schemas and a question, generate a correct SQLlite query."

def format_schema_block(table_schemas: List[Tuple[str, str]]) -> str:
    """
    Takes a list of (table_name, schema_text) and formats into LLM-readable form.
    Example:
        -- Table: customer
        customer_id, first_name, last_name, ...

        -- Table: payment
        payment_id, customer_id, amount, ...
    """
    result = ""
    for table_name, schema_text in table_schemas:
        result += f"-- Table: {table_name}\n{schema_text.strip()}\n\n"
    return result.strip()

def build_prompt(user_question: str, table_schemas: List[Tuple[str, str]]) -> str:
    """
    Combines the system instruction, table schemas, and user question into a final LLM prompt.
    """
    schema_section = format_schema_block(table_schemas)

    prompt = f"""{SYSTEM_INSTRUCTION}

{schema_section}

-- User Question:
{user_question}

-- Write only the SQL query. Do not explain.\n\n```sql\n

-- Never returns id's or primary keys in the result unless explicitly asked.

-- Always use LIMIT 100 to avoid large results.
-- Always return the quantitative results.
-- Always return Name as including first_name and last_name.
-- Never return more than 100 rows.
```sql
"""
    return prompt

# ✅ Optional: Few-shot examples you can feed into LLM for better results
FEW_SHOT_EXAMPLES = [
    {
        "question": "Get the top 5 customers by total payment amount.",
        "schema_hint": ["payment", "customer"],
        "sql": """SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total DESC
LIMIT 5;"""
    }
    # Add more if needed
]
