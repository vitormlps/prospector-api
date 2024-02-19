from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..entities.flight_route.schema import FlightRouteShow
from ..entities.aircraft.schema import AircraftShow


class MissionBase(BaseModel):
    position: int
    status: Optional[str] = Field(min_length=1, max_length=25)
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    user_id: UUID
    inspection_id: int
    aircraft_id: int
    flight_route_id: int


class MissionCreate(MissionBase):
    pass


class MissionUpdate(MissionBase):
    id: int
    position: Optional[int]
    user_id: Optional[UUID]
    inspection_id: Optional[int]
    aircraft_id: Optional[int]
    flight_route_id: Optional[int]


class MissionShow(MissionBase):
    id: int
    aircraft: AircraftShow
    flight_route: FlightRouteShow
    created_at: datetime
    updated_at: Optional[datetime]


    def dict(self, **kwargs):
        kwargs['exclude'] = {'aircraft_id', 'flight_route_id'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'aircraft_id', 'flight_route_id'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
