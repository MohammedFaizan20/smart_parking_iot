import json
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv(verbose=True)

class Settings(BaseSettings):
    # jwt token set-up parameter
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    #mongo credentials
    mongo_url:str
    db_name:str
    sql_db_url: str

    class Config:
        env_file = ".env"

settings = Settings()
