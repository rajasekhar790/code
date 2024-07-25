@bscdata1.route("/select", methods=["POST"])
async def select_table(request):
    schema = request.json
    table_name = schema.get("table_name")

    if not table_name:
        return json({"error": "Table name is missing."})

    select_query = f"SELECT * FROM {table_name};"

    try:
        logger.info(f"Executing query: {select_query}")
        cursor = connection.execute_query(select_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        result = [dict(zip(columns, row)) for row in rows]
        return json({"data": result})
    except Exception as e:
        logger.error(f"Error selecting from table {table_name}: {e}")
        return json({"error": "An error occurred while fetching data from the table."})
