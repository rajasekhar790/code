from sanic import Sanic, response
from sanic.request import Request
import pandas as pd
from io import BytesIO
import psycopg2
from datetime import datetime

app = Sanic("ExcelUploader")

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname='your_db_name',
        user='your_username',
        password='your_password',
        host='your_host',
        port='your_port'
    )

# Route to upload Excel file
@app.post("/upload")
async def upload(request: Request):
    if 'file' not in request.files:
        return response.text("File not found", status=400)

    file = request.files.get('file')[0].body

    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(BytesIO(file))

    conn = get_db_connection()

    # Using context manager for database connection and cursor
    with conn:
        with conn.cursor() as cursor:
            for index, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO cpt_ppp_flags (
                        record_type, client_id, loc, state_of_issuance, product_code, employer_group, network_code, funding_type,
                        test_name, cpt, second_pathology_read_indicator, sub_specialty_medical_credentials_indicator,
                        cap_accreditation_indicator, e_orders_results_indicator, valid_begin_date, valid_end_date, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row['record_type'], row['client_id'], row['lob'], row['state_of_issuance'], row['product_code'],
                        row['employer_group'], row['network_code'], row['funding_type'], row['test_name'], row['cpt'],
                        row['second_pathology_read_indicator'], row['sub_specialty_medical_credentials_indicator'],
                        row['cap_accreditation_indicator'], row['e_orders_results_indicator'], row['valid_begin_date'],
                        row['valid_end_date'], datetime.now()
                    )
                )

    return response.json({"message": "Data upload successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
