from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json, text
import dbconnection
import pandas as pd
from io import BytesIO, StringIO
from datetime import datetime

app = Sanic("Application")
connection = dbconnection.connect()

@app.route("/")
async def index(request):
    return response.text("Welcome to the Excel to PostgreSQL uploader!")

@app.post("/upload")
async def upload(request: Request):
    if 'file' not in request.files:
        return text("File not found", status=400)

    file = request.files.get('file')
    if not file:
        return text("File not found in the request", status=400)

    try:
        # Read the Excel file into a Pandas DataFrame, skipping the first row
        df = pd.read_excel(BytesIO(file.body))

        # Add a 'created_at' column with the current timestamp
        df['created_at'] = pd.Timestamp.now()

        # Print DataFrame for debugging
        print(df.head())
        print(df.columns)

        cur = connection.cursor()
        try:
            # Truncate the table before loading new data
            cur.execute("TRUNCATE table cpt_ppp_flags")

            # Convert DataFrame to CSV
            buffer = StringIO()
            df.to_csv(buffer, index=False, header=False)
            buffer.seek(0)

            # Use copy_from to bulk insert the data
            cur.copy_from(buffer, 'cpt_ppp_flags', sep=',')
        except Exception as e:
            connection.rollback()
            print(f"Error during data insertion: {e}")
            return response.text(f"An error occurred during data insertion: {e}", status=500)
        else:
            connection.commit()
        finally:
            cur.close()
    except Exception as e:
        print(f"Error processing the file: {e}")
        return response.text(f"An error occurred while processing the file: {e}", status=500)
    finally:
        connection.close()

    return response.json({"message": "Data upload successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
