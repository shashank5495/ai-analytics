import requests
import re

SYSTEM_PROMPT = """
You are an expert PostgreSQL SQL generator for Aroma House ERP database.

STRICT RULES:
1. Only generate SELECT queries
2. ALWAYS filter inactive = 'N'
3. ALWAYS filter cancelled = 'N' for transactional tables
4. Use rpt_stock_balance for stock, sales, and analytics queries

IMPORTANT TIME RULE:
- fiscal_year is INTEGER
- FY 2025-26 = 26
- FY 2024-25 = 25
- DO NOT use date strings like '2025-01'
- ALWAYS use fiscal_year = <number>

5. Use joins properly between mst_item and rpt_stock_balance
6. Output ONLY SQL
7. SQL must start with SELECT

SCHEMA:
mst_item (item_id, item_name, item_type, inactive)
rpt_stock_balance (fiscal_year, item_id, receipt_qty, issue_qty, closing_qty)
"""

def extract_sql(text):
    # Extract SQL starting from SELECT
    match = re.search(r"(SELECT .*?;)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()

def generate_sql(user_query):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": SYSTEM_PROMPT + "\nUser: " + user_query,
            "stream": False
        }
    )

    raw_output = response.json()["response"]

    clean_sql = extract_sql(raw_output)

    return clean_sql