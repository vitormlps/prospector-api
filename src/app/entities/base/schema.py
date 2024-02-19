from pydantic import BaseModel
from typing import Optional


class DefaultQueryFilter(BaseModel):
    unit_id: int
    skip: Optional[int]
    limit: Optional[int]
