from pydantic import BaseModel
from models.train.train_request import DatasetPrototype

class RequestTrain(BaseModel):
    name: str
    description: str | None = None
    dataset_prototype: DatasetPrototype
    train_ratio: float = 0.8
class RunTrain(BaseModel):
    id: int