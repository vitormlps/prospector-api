from typing import Optional, Any, List
from datetime import datetime, date

from pydantic import BaseModel, Field, root_validator

from ..entities.thermal_data.schema import ThermalDataShow
from ..entities.component.schema import ComponentShow
from ..utils.georefs import parse_location_to_array
from ..entities.base.schema import DefaultQueryFilter


class EquipmentBase(BaseModel):
    id: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=200)
    denomination: Optional[str] = Field(min_length=1, max_length=30)
    operational_area: Optional[str] = Field(min_length=1, max_length=3)
    latitude: Optional[float]
    longitude: Optional[float]
    tension: Optional[str] = Field(max_length=10)
    manufacturer: Optional[str] = Field(max_length=120)
    manufactured_at: Optional[date]
    bay_id: int
    thermal_data_id: Optional[int]
    type_id: Optional[int]


class EquipmentCreate(EquipmentBase):
    latitude: float
    longitude: float


class EquipmentUpdate(EquipmentBase):
    name: Optional[str]
    location: Optional[Any]
    bay_id: Optional[int]


class EquipmentShow(EquipmentBase):
    location: Optional[Any]
    created_at: datetime
    updated_at: Optional[datetime]
    image_count: Optional[int]
    analyzed_image_count: Optional[int]
    anomaly_count: Optional[int]
    last_inspection_id: Optional[int]

    @root_validator
    def format_fields(cls, values: dict) -> dict:
        if values["location"]:
            location = parse_location_to_array(values["location"])
            values["location"] = location
            values["latitude"], values["longitude"] = location
        return values

    class Config:
        orm_mode = True


class EquipmentsComponents(EquipmentShow):
    components: List[ComponentShow]


class EquipmentsThermal(EquipmentShow):
    thermal_data: Optional[ThermalDataShow]

    def dict(self, *args, **kwargs):
        kwargs['exclude'] = {'thermal_data_id'}
        return super().dict(*args, **kwargs)

    def json(self, *args, **kwargs):
        kwargs['exclude'] = {'thermal_data_id'}
        return super().json(*args, **kwargs)


class EquipmentQuery(DefaultQueryFilter):
    name: Optional[str]
    description: Optional[str]
    denomination: Optional[str]
    location: Optional[str]
    bay_id: Optional[int]
    inspection_id: Optional[int]
