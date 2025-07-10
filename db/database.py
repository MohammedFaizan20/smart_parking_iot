from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import create_engine, Column, Boolean, Float, Integer, String
from db.config import settings

Base = declarative_base()

engine = create_engine(settings.sql_db_url)

Base.metadata.bind = engine
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
