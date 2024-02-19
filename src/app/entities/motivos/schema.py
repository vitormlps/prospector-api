from typing import Optional, List, Union, Any
from datetime import datetime, date, timedelta

from fastapi import Query
from pydantic import BaseModel, Field, root_validator, validator

from ..entities.anomaly_tag_in_component.schema import AnomalyTagInComponentShow

# from ..entities.comment.schema import CommentShow
from ..utils.georefs import parse_location_to_array

from ..entities.inspection_equipment.schema import (
    InspectionEquipmentShowWithoutImages,
)


class ImageBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    is_analyzed: bool
    flight_yaw: float
    lens_fov: float
    gimbal_pitch: Optional[float]
    shot_taken_at: Optional[datetime]
    source_type: Optional[str] = Field(min_length=1, max_length=30)
    inspection_equipment_id: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    location: Optional[List[List[float]]] | Optional[str]


class ImageCreate(ImageBase):
    pass


class ImageUpdate(BaseModel):
    is_analyzed: bool


class ImageShow(ImageBase):
    id: int
    url: Optional[str]
    thumb: Optional[str]
    anomaly_tags_in_component: List[AnomalyTagInComponentShow]
    # comments: List[CommentShow]
    created_at: datetime
    updated_at: Optional[datetime]

    @root_validator
    def format_fields(cls, values: dict) -> dict:
        if values["location"]:
            location = parse_location_to_array(values["location"])
            # TODO: Remove key
            values["location"] = None
            values["latitude"], values["longitude"] = location
        return values

    inspection_equipment: Optional[InspectionEquipmentShowWithoutImages]

    class Config:
        orm_mode = True


class ImageShowHighRes(BaseModel):
    images: Optional[List[ImageShow]]
    detail: Optional[str]


class ImageShowThermal(BaseModel):
    thermal_matrix: Optional[List[List[float]]]
    x_max: Optional[float]
    x_mean: Optional[float]
    x_min: Optional[float]


class ImageQuery(BaseModel):
    inspection_id: Optional[int]
    equipment_id: Optional[str]
    skip: Optional[int]
    limit: Optional[int]


class ImageQueryV2(BaseModel):
    inspection_id: Optional[int]
    equipment_id: Optional[str]
    anomalies: Optional[List[int]] = Field(Query([]))
    source_types: Optional[List[str]] = Field(Query([]))
    components: Optional[List[int]] = Field(Query([]))
    is_analyzed: Optional[bool]
    order_by: Optional[str]
