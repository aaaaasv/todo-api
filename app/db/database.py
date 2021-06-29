from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_HOST}/{settings.SQL_DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
