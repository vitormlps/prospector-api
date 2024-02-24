#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps


class MunicipiosBase(BaseModel):
    codigo: str
    nome: str = Field(min_length=3)
    uf: str = Field(min_length=2, max_length=2)


class MunicipiosCreate(MunicipiosBase):
    pass


class MunicipiosUpdate(MunicipiosBase):
    id: UUID
    codigo: Optional[str]
    nome: Optional[str] = Field(min_length=3)
    uf: Optional[str] = Field(min_length=2, max_length=2)


class MunicipiosShow(MunicipiosBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
