from sanic import Sanic
from sanic.response import json, text
from sanic.request import Request
import psycopg2
from psycopg2 import sql
import datetime  


app = Sanic("DynamicTableApp")

# Database configuration
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': '5432'
}

# Function to get database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def initialize_metadata_table():
    conn = get_db_connection()
    create_metadata_table_sql = """
    CREATE TABLE IF NOT EXISTS metadata (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(255) NOT NULL,
        column_name VARCHAR(255) NOT NULL,
        column_type VARCHAR(255) NOT NULL,
        column_constraints VARCHAR(255)
    );
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_metadata_table_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creating metadata table: {e}")
    finally:
        conn.close()

initialize_metadata_table()

@app.route("/create_table", methods=["POST"])
async def create_table(request: Request):
    schema = request.json
    table_name = schema["table_name"]
    columns = schema["columns"]

    column_definitions = []
    metadata_entries = []
    for column in columns:
        name = column["name"]
        data_type = column["type"]
        constraints = column.get("constraints", "")
        column_definitions.append(f"{name} {data_type} {constraints}")
        metadata_entries.append((table_name, name, data_type, constraints))

    columns_sql = ", ".join(column_definitions)
    create_table_sql = f"CREATE TABLE {table_name} ({columns_sql});"

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            insert_metadata_sql = """
            INSERT INTO metadata (table_name, column_name, column_type, column_constraints)
            VALUES (%s, %s, %s, %s);
            """
            cursor.executemany(insert_metadata_sql, metadata_entries)
        conn.commit()
        return text(f"Table {table_name} created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error creating table: {e}")
        return text(f"Error creating table: {e}", status=500)
    finally:
        conn.close()

@app.route("/insert_data", methods=["POST"])
async def insert_data(request: Request):
    data = request.json
    table_name = data["table_name"]
    records = data["records"]

    if not records:
        return text("No records provided.", status=400)

    columns = records[0].keys()
    columns_sql = ", ".join(columns)
    values_sql = ", ".join([f"%({col})s" for col in columns])

    insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(columns_sql),
        sql.SQL(values_sql)
    )
    print(insert_sql)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.executemany(insert_sql.as_string(conn), records)
        conn.commit()
        return text(f"Data inserted successfully into {table_name}.")
    except Exception as e:
        conn.rollback()
        return text(f"Error inserting data: {e}", status=500)
    finally:
        conn.close()

@app.route("/select", methods=["POST"])
async def select_data(request: Request):
    data = request.json
    table_name = data["table_name"]

    select_sql = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            result = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                for key, value in row_dict.items():
                    if isinstance(value, (datetime.date, datetime.datetime)):
                        row_dict[key] = value.isoformat()
                    else:
                        row_dict[key] = str(value)
                result.append(row_dict)
                
        return json(result)
    except Exception as e:
        return text(f"Error retrieving data: {e}", status=500)
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
