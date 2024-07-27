import os
from sanic import Sanic, Blueprint
from sanic.response import json, text
import logging
from sanic.request import Request
import json as json_lib
import datetime
from xpms_storage.db_handler import DBProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database connection instance
connection = DBProvider.get_instance(db_name="claimsol3")

bscdata1 = Blueprint('bscdata1')

@bscdata1.route("/select", methods=["POST"])
async def select_table(request):
    schema = request.json
    table_name = schema.get("table_name")

    if not table_name:
        return json({"error": "Table name is missing."})

    try:
        # Check if the table exists
        check_table_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}');"
        logger.info(f"Executing query: {check_table_query}")
        cursor = connection.execute_query(check_table_query)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            return json({"error": f"Table {table_name} does not exist."})

        # Fetch data from the table
        select_query = f"SELECT * FROM {table_name};"
        logger.info(f"Executing query: {select_query}")
        cursor = connection.execute_query(select_query)
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]

        return json({"success": f"Data fetched successfully from {table_name}.", "data": data})
    except Exception as e:
        logger.error(f"Error selecting from table {table_name}: {e}")
        return json({"error": "An error occurred while selecting data from the table."})

if __name__ == "__main__":
    app = Sanic(__name__)
    app.blueprint(bscdata1)
    app.run(host="0.0.0.0", port=8000)
