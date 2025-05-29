from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
class UserLogin(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"