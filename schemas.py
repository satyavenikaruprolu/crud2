from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class PasswordCreate(BaseModel):
    site_name: str
    site_url: str
    username: str
    password: str

class Password(BaseModel):
    id: int
    user_id: int
    site_name: str
    site_url: str
    username: str
    password: str

    class Config:
        orm_mode = True
