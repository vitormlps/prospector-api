#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps
from ..paises.schema import PaisesView
from ..municipios.schema import MunicipiosView


class LogradourosBase(BaseModel):
    tipo: str = Field(min_length=3)
    nome: str = Field(min_length=3)
    nome_cidade_exterior: Optional[str] = Field(min_length=3)
    numero: Optional[str] = Field(min_length=1)
    complemento: Optional[str] = Field(min_length=1)
    bairro: Optional[str] = Field(min_length=3)
    cep: str = Field(min_length=8, max_length=8)
    municipio_id: UUID
    pais_id: Optional[UUID]


class LogradourosCreate(LogradourosBase):
    pass


class LogradourosUpdate(LogradourosBase):
    id: UUID
    tipo: Optional[str] = Field(min_length=3)
    nome: Optional[str] = Field(min_length=3)
    cep: Optional[str] = Field(min_length=8, max_length=8)
    municipio_id: Optional[UUID]


class LogradourosShow(LogradourosBase):
    id: UUID
    municipio: MunicipiosView
    pais: Optional[PaisesView]
    created_at: datetime
    updated_at: datetime

    def dict(self, **kwargs):
        kwargs['exclude'] = {'municipio_id', 'pais_id'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'municipio_id', 'pais_id'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
