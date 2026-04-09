import psycopg2

def run_sql(query):
    conn = psycopg2.connect(
        dbname="aroma_house",
        user="postgres",
        password="Shash@2004",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute(query)

    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"columns": columns, "rows": rows}