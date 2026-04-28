def validate_query(query):
    q = query.lower()

    if not q.startswith("select"):
        raise Exception("Only SELECT queries allowed")

    blocked = ["delete", "update", "insert", "drop", "alter"]
    for word in blocked:
        if word in q:
            raise Exception("Unsafe query detected")

    if "invoice_id" in q:
        raise Exception("Use linv_id instead of invoice_id")

    if "join" in q and " on " not in q:
        raise Exception("JOIN missing ON condition")

    if "mst_item.item_id = local_invoice_header" in q:
        raise Exception("Invalid join: use local_invoice_detail as bridge")

    if "hexagon" in q and "group_code" not in q:
        raise Exception("Must filter using group_code for item group queries")

    return True
