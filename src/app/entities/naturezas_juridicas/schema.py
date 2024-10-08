#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps


class NaturezasJuridicasBase(BaseModel):
    codigo: str
    descricao: str = Field(min_length=3)


class NaturezasJuridicasCreate(NaturezasJuridicasBase):
    pass


class NaturezasJuridicasUpdate(NaturezasJuridicasBase):
    id: UUID
    codigo: Optional[str]
    descricao: Optional[str] = Field(min_length=3)


class NaturezasJuridicasView(NaturezasJuridicasBase):
    id: UUID
    descricao: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
