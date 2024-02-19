from typing import Optional, Any #, List
from datetime import datetime

from pydantic import BaseModel, Field, root_validator

# from ..entities.action.schema import ActionShow
from ..utils.georefs import parse_location_to_array


class WaypointBase(BaseModel):
    position: int
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: float
    speed: float
    heading_angle: float
    gimbal_pitch: int
    corner_radius: float
    turn_mode: Optional[str] = Field(min_length=1, max_length=30)
    flight_route_id: int


class WaypointCreate(WaypointBase):
    latitude: float
    longitude: float


class WaypointUpdate(WaypointBase):
    id: int
    position: Optional[int]
    location: Optional[Any]
    altitude: Optional[float]
    speed: Optional[float]
    heading_angle: Optional[float]
    gimbal_pitch: Optional[int]
    corner_radius: Optional[float]
    flight_route_id: Optional[int]


class WaypointShow(WaypointBase):
    id: int
    location: Optional[Any]
    # actions: List[ActionShow]
    created_at: datetime
    updated_at: Optional[datetime]

    @root_validator
    def format_fields(cls, values: dict) -> dict:
        if values["location"]:
            location = parse_location_to_array(values["location"])
            values["location"] = location
            values["latitude"], values["longitude"] = location
        return values

    # def dict(self, **kwargs):
    #     self.location = parse_location_to_array(self.location)
    #     return super().dict(**kwargs)

    # def json(self, **kwargs):
    #     self.location = parse_location_to_array(self.location)
    #     return super().json(**kwargs)

    class Config:
        orm_mode = True
