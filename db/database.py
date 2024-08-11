from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import create_engine, Column, Boolean, Float, Integer, String


Base = declarative_base()

# engine = create_engine("mysql+pymysql://root:Usersnp!98@localhost/parking")

engine = create_engine("mysql+pymysql://root:Userlogin!123@127.0.0.1/parking")

Base.metadata.bind = engine
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()