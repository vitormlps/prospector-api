#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps


class PaisesBase(BaseModel):
    codigo: str
    nome: str = Field(min_length=3)


class PaisesCreate(PaisesBase):
    pass


class PaisesUpdate(PaisesBase):
    id: UUID
    codigo: Optional[str]
    nome: Optional[str] = Field(min_length=3)


class PaisesView(PaisesBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
