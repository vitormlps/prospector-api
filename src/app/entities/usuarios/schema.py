from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

from ..entities.user_type.schema import UserTypeShow


class UserBase(BaseModel):
    id: UUID
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    is_superuser: bool = Field(default=False)
    is_active: Optional[bool] = Field(default=True)
    type_id: int
    company_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_superuser: Optional[bool]
    type_id: Optional[int]
    company_id: Optional[int]


class UserShow(UserBase):
    type: UserTypeShow
    created_at: datetime
    updated_at: Optional[datetime]

    def dict(self, **kwargs):
        kwargs['exclude'] = {'type_id', 'password'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'type_id', 'password'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
