from fastapi import FastAPI
from pydantic import BaseModel
from llm import generate_sql
from query_executor import run_sql
from guardrails import validate_query
import webbrowser

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


@app.on_event("startup")
def open_browser():
    webbrowser.open("http://127.0.0.1:8000/docs")


@app.get("/")
def home():
    return {"message": "AI Analytics API is running"}


def is_time_query(question):
    keywords = ["sales", "trend", "monthly", "year", "fy"]
    return any(k in question.lower() for k in keywords)


@app.post("/query")
def ask(data: QueryRequest):
    try:
        user_question = data.question

        if is_time_query(user_question) and "fy" not in user_question.lower():
            return {
                "message": "Please specify timeframe (e.g., current FY, last FY)"
            }
        sql = generate_sql(user_question)
        print("Generated SQL:", sql)

        validate_query(sql)

        result = run_sql(sql)

        return {
            "question": user_question,
            "sql": sql,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}