def validate_query(query):
    q = query.lower().strip()

    if not q.startswith("select"):
        raise Exception("Only SELECT queries allowed")

    blocked = ["delete", "update", "insert", "drop", "alter", "truncate"]
    for word in blocked:
        if word in q:
            raise Exception("Unsafe query detected")

    return True