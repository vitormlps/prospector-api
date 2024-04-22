#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps
from ..municipios.schema import MunicipiosView
from ..base.schema import DefaultQueryFilter


class LogradourosBase(BaseModel):
    tipo: str = Field(min_length=3)
    nome: str = Field(min_length=3)
    numero: Optional[str] = Field(min_length=1)
    complemento: Optional[str] = Field(min_length=1)
    bairro: Optional[str] = Field(min_length=3)
    cep: str = Field(min_length=8, max_length=8)
    estado_uf: str = Field(min_length=2, max_length=2)
    municipio_id: UUID


class LogradourosCreate(LogradourosBase):
    pass


class LogradourosUpdate(LogradourosBase):
    id: UUID
    tipo: Optional[str] = Field(min_length=3)
    nome: Optional[str] = Field(min_length=3)
    cep: Optional[str] = Field(min_length=8, max_length=8)
    estado_uf: Optional[str] = Field(min_length=2, max_length=2)
    municipio_id: Optional[UUID]


class LogradourosView(LogradourosBase):
    id: UUID
    tipo: str
    nome: str
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cep: str
    estado_uf: str
    # municipio: MunicipiosView
    created_at: datetime
    updated_at: datetime

    # def dict(self, **kwargs):
    #     kwargs['exclude'] = {'municipio_id'}
    #     return super().dict(**kwargs)

    # def json(self, **kwargs):
    #     kwargs['exclude'] = {'municipio_id'}
    #     return super().json(**kwargs)

    class Config:
        orm_mode = True


class LogradourosFilter(DefaultQueryFilter):
    tipo: Optional[str]
    nome: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cep: Optional[str]
    estado_uf: Optional[str]
    municipio_id: Optional[UUID]