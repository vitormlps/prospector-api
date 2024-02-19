from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class UserTypeModel(BaseModel):
    name: str = Field(min_length=1, max_length=30)


class UserTypeCreate(UserTypeModel):
    pass


class UserTypeUpdate(UserTypeModel):
    id: int
    name: Optional[str]


class UserTypeShow(UserTypeModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
