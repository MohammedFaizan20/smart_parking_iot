import datetime
from typing import List, Optional,Any,Union
from pydantic import AnyUrl, BaseModel, Field,validator


class User(BaseModel):
    email: str
    password: str
    confirm_password: str
    full_name: str
    agree_terms:bool


class UserLogIn(BaseModel):
    email: str
    password: str


class ParkingData(BaseModel):
    api_key: str
    value:int