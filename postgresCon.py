
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
