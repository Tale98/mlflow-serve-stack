from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from pydantic import EmailStr
from typing import Optional
import datetime
from utils.datetime.timestamp import timestamp
from enum import Enum
class TrainRequestStatus(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
class DatasetPrototype(str, Enum):
    iris = "iris"
    wine = "wine"

class TrainRequestTableBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    description: Optional[str] = None
class TrainRequestTable(TrainRequestTableBase, table=True):  # Defines as a table
    __tablename__ = "train_requests"
    user_id: int = Field(foreign_key="users.id")
    dataset_prototype: DatasetPrototype
    train_ratio: float = Field(default=0.8, ge=0.0, le=1.0)
    binded_run_uuid: str = Field(default=None, nullable=True)
    status: TrainRequestStatus = Field(default=TrainRequestStatus.WAITING)
    created_at: datetime.datetime = Field(default_factory=timestamp, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime.datetime = Field(default_factory=timestamp, sa_column=Column(DateTime(timezone=True)))
