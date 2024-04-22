#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps
from ..base.schema import DefaultQueryFilter


class ContatosBase(BaseModel):
    tipo: str = Field(min_length=3)
    descricao: str = Field(min_length=3)
    estabelecimento_id: UUID


class ContatosCreate(ContatosBase):
    pass


class ContatosUpdate(ContatosBase):
    id: UUID
    tipo: Optional[str] = Field(min_length=3)
    descricao: Optional[str] = Field(min_length=3)
    estabelecimento_id: Optional[UUID]


class ContatosView(ContatosBase):
    id: UUID
    tipo: str
    descricao: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ContatosFilter(DefaultQueryFilter):
    tipo: Optional[str]
    descricao: Optional[str]
    estabelecimento_id: Optional[UUID]
