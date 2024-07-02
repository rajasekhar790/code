from sanic import Sanic, Blueprint, response
from sanic.request import Request
import asyncpg
import os

app = Sanic("CreateTableAPI")
bscdata1 = Blueprint('bscdata1')

async def create_db_connection():
    connection = await asyncpg.create_pool(
        user='your_user', 
        password='your_password', 
        database='your_database', 
        host='your_host', 
        port=os.getenv('DB_PORT', 5432)
    )
    print("Connection to PostgreSQL DB successful")
    return connection

@app.listener('before_server_start')
async def setup_db(app, loop):
    app.ctx.db = await create_db_connection()

@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.ctx.db.close()

@bscdata1.route("/create_table", methods=["GET", "POST"])
async def create_table(request: Request):
    try:
        data = request.json
        table_name = data["table_name"]
        columns = data["columns"]
        
        columns_sql = ", ".join([f"{col['name']} {col['type']}" for col in columns])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
        
        async with app.ctx.db.acquire() as connection:
            await connection.execute(create_table_sql)
        
        return response.json({"status": "success", "table": table_name, "sql": create_table_sql, "message": "Table created successfully"})
    
    except Exception as e:
        return response.json({"status": "fail", "message": f"Error: {e}"})

@bscdata1.route("/update_table", methods=["GET", "POST"])
async def update_table(request: Request):
    try:
        data = request.json
        table_name = data["table_name"]
        rows = data["rows"]
        
        async with app.ctx.db.acquire() as connection:
            async with connection.transaction():
                for row in rows:
                    columns = ", ".join(row.keys())
                    values = ", ".join([f"${i+1}" for i in range(len(row))])
                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) ON CONFLICT (your_primary_key) DO UPDATE SET {columns} = EXCLUDED.{columns};"
                    await connection.execute(query, *row.values())
        
        return response.json({"status": "success", "table": table_name, "message": "Table updated successfully"})
    
    except Exception as e:
        return response.json({"status": "fail", "message": f"Error: {e}"})

app.blueprint(bscdata1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)