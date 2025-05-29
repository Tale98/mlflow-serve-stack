from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from pydantic import EmailStr
from typing import Optional
import datetime
from utils.datetime.timestamp import timestamp
class UserBase(SQLModel):
    username: str
    email: EmailStr = Field(unique=True)

class User(UserBase, table=True):  # Defines as a table
    __tablename__ = "users" 
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = False
    created_at: datetime.datetime = Field(default_factory=timestamp, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime.datetime = Field(default_factory=timestamp, sa_column=Column(DateTime(timezone=True)))