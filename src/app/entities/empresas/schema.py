from typing import Optional, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..entities.mission.schema import MissionShow
from ..entities.equipment.schema import EquipmentShow


class InspectionBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=200)
    status: Optional[str] = Field(min_length=1, max_length=25)
    type: str = Field(min_length=1, max_length=30)
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    unit_id: int
    user_id: UUID

class InspectionCreate(InspectionBase):
    pass


class InspectionUpdate(InspectionBase):
    id: int
    name: Optional[str]
    type: Optional[str]
    unit_id: Optional[int]
    user_id: Optional[UUID]


class InspectionShow(InspectionBase):
    id: int
    missions: List[MissionShow]
    equipments: Optional[List[EquipmentShow]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class LastInspectionShow(InspectionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
