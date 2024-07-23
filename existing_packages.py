import os
from sanic import Sanic, Blueprint
from sanic.response import json, text
from sanic.request import Request
import logging
import json as json_lib
import datetime
from xpms_storage.db_handler import DBprovider
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database connection instance
connection = DBprovider.get_instance()

bscdata1 = Blueprint('bscdata1')

@bscdata1.route("/create_table", methods=["POST"])
async def create_table(request: Request):
    schema = request.json
    table_name = schema.get("table_name")
    columns = schema.get("columns")

    if not table_name or not columns:
        return json({"error": "Table name or columns are missing. Table creation is aborted."}, status=400)

    if isinstance(columns, dict):
        columns = [columns]

    column_definitions = []
    for column in columns:
        name = column.get("name")
        data_type = column.get("type")
        constraints = column.get("constraints", "")
        if not name or not data_type:
            return json({"error": "Column name or type is missing. Table creation is aborted."}, status=400)
        column_definitions.append(f"{name} {data_type} {constraints}")

    columns_sql = ", ".join(column_definitions)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"

    try:
        # Check if the table exists
        check_table_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
        table_exists = connection.execute_query(check_table_query).fetchone()[0]

        if table_exists:
            return json({"message": f"Table {table_name} already exists."}, status=200)
        
        # Create the table
        connection.execute_query(create_table_sql)
        return json({"message": f"Table {table_name} created successfully."}, status=200)
    except SQLAlchemyError as e:
        logger.error(f"Error creating table: {e}")
        return json({"error": f"Error creating table: {str(e)}"}, status=500)

# Sanic application initialization
app = Sanic(__name__)
app.blueprint(bscdata1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
