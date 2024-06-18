
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)

# Database configuration
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'
DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'your_db_name'
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

-------------------------------------------------------------------------------------------------------------------------------


from sanic import Sanic, response
from sanic.request import File
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from io import BytesIO

# Database configuration
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'
DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'your_db_name'
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
engine = create_engine(DB_URL)

# Create a function to generate a new session
def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

# Create Sanic app
app = Sanic("ExcelToPostgres")

# Initialize the database
Base.metadata.create_all(engine)

@app.post("/upload")
async def upload(request):
    if 'file' not in request.files:
        return response.json({'error': 'No file uploaded'}, status=400)

    file: File = request.files.get('file')
    if not file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return response.json({'error': 'Invalid file type'}, status=400)

    # Read Excel file into a DataFrame
    try:
        data = pd.read_excel(BytesIO(file.body))
    except Exception as e:
        return response.json({'error': str(e)}, status=500)

    # Create a new session
    session = get_session()

    # Truncate the table and insert new data
    try:
        session.query(User).delete()
        for _, row in data.iterrows():
            user = User(name=row['name'], age=row['age'], email=row['email'])
            session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        return response.json({'error': str(e)}, status=500)
    finally:
        session.close()

    return response.json({'status': 'success'}, status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
