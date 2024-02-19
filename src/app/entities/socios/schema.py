from typing import Optional #, List
from datetime import datetime

from pydantic import BaseModel, Field

# from ..entities.waypoint.schema import WaypointShow


class FlightRouteBase(BaseModel):
    auto_flight_speed: Optional[float]
    max_flight_speed: Optional[float]
    is_exit_mission_on_rc_signal_lost_enabled: bool
    timelapse: Optional[int]
    go_to_waypoint_mode: str = Field(min_length=1, max_length=30)
    path_mode: str = Field(min_length=1, max_length=30)
    heading_mode: str = Field(min_length=1, max_length=30)
    finished_action: str = Field(min_length=1, max_length=30)


class FlightRouteCreate(FlightRouteBase):
    pass


class FlightRouteUpdate(FlightRouteBase):
    id: int
    is_exit_mission_on_rc_signal_lost_enabled: Optional[bool]
    go_to_waypoint_mode: Optional[str]
    path_mode: Optional[str]
    heading_mode: Optional[str]
    finished_action: Optional[str]


class FlightRouteShow(FlightRouteBase):
    id: int
    # waypoints: List[WaypointShow]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
