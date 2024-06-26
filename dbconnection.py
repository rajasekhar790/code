import os
import psycopg2
from psycopg2 import OperationalError

def create_db_connection():
    try:
        # Get database connection parameters from environment variables
        db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'localhost'),  # Default to 'localhost' if not set
            'port': os.getenv('DB_PORT', 5432)  # Default to 5432 if not set
        }
        
        # Create a new database connection
        connection = psycopg2.connect(**db_params)
        print("Connection to PostgreSQL DB successful")
        return connection
    except OperationalError as e:
        print(f"Error: '{e}' occurred while connecting to the PostgreSQL database")
        return None

# Usage example
if __name__ == "__main__":
    conn = create_db_connection()
    if conn:
        # Do something with the connection
        conn.close()