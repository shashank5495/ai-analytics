import requests
import re

SYSTEM_PROMPT = """
You are an expert PostgreSQL SQL generator.

STRICT RULES:
- Only SELECT queries
- Use ONLY given tables and columns
- ALWAYS use correct JOIN conditions

TABLES:

mst_item(item_id, item_name, item_type, group_code, inactive)
mst_item_group(group_code, group_name)
rpt_stock_balance(fiscal_year, item_id, receipt_qty, issue_qty, closing_qty)
local_invoice_header(linv_id, linv_no, linv_date, customer_id, cancelled)
local_invoice_detail(linv_detail_id, linv_id, item_id, linv_qty, linv_rate, linv_amount)

RELATIONSHIPS:
- local_invoice_header.linv_id = local_invoice_detail.linv_id
- mst_item.item_id = local_invoice_detail.item_id
- mst_item.item_id = rpt_stock_balance.item_id

RULES:
- Sales → use local_invoice tables
- Stock → use rpt_stock_balance
- If item_name needed → JOIN mst_item
- ALWAYS use correct ON condition
- ALWAYS filter cancelled = 'N' for invoice tables

JOIN RULES (STRICT):
- NEVER join mst_item directly with local_invoice_header
- mst_item must join ONLY with local_invoice_detail using item_id
- local_invoice_header must join ONLY with local_invoice_detail using linv_id
- Always follow this path:
-mst_item → local_invoice_detail → local_invoice_header
- For item group filtering, ALWAYS use group_code
- NEVER filter using item_name for group queries

RELATIONSHIPS:
- mst_item.item_id = local_invoice_detail.item_id
- local_invoice_header.linv_id = local_invoice_detail.linv_id
- mst_item.group_code = mst_item_group.group_code

IMPORTANT DATE RULE:
- Do NOT use date_trunc
- Use BETWEEN for date filtering
- FY 2025-26 means:
-linv_date BETWEEN '2025-04-01' AND '2026-03-31'
IMPORTANT:
- fiscal_year is integer
- FY 2025-26 = 26

RETURN ONLY SQL QUERY.
"""

def extract_sql(text):
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
