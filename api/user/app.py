from api.schema import *
import bcrypt
from fastapi import Body, APIRouter,Query, HTTPException
from sqlalchemy import create_engine, Column, Boolean, Float, Integer, String
from db.database import Base,get_db,engine
from fastapi import Request, FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, declarative_base


# authenticate router
public_router = APIRouter()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200))
    email = Column(String(200), unique=True, index=True)
    password = Column(String(200))
    agree_terms = Column(Boolean)


# Create database tables
Base.metadata.create_all(bind=engine)


# Define API endpoints
@public_router.post("/signup/")
async def signup(user: dict, db: Session = Depends(get_db)):
    if not user.get("agree_terms"):
        raise HTTPException(status_code=400, detail="Agree to terms and conditions")

    user_exists = db.query(User).filter(User.email == user.get("email")).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.get("password").encode('utf-8'), bcrypt.gensalt())
    user["password"] = hashed_password.decode('utf-8')
    user.pop("confirm_password")
    db.add(User(**user))
    db.commit()
    db.close()
    return {"message": "User registered successfully"}


@public_router.post("/login")
async def login(user: dict, db: Session = Depends(get_db)):
    stored_user = db.query(User).filter(User.email == user.get("email")).first()
    email = user.get("email")
    if not stored_user:
        raise HTTPException(status_code=500, detail="Email not found")

    stored_password = stored_user.password
    if not bcrypt.checkpw(user.get("password").encode('utf-8'), stored_password.encode('utf-8')):
        raise HTTPException(status_code=500, detail="Invalid password")

    return {"status": "true","data":{"email":email}}