#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel

# ### Local deps
from ..base.schema import DefaultQueryFilter


class SimplesNacionalBase(BaseModel):
    opcao_simples: bool
    data_opcao_simples: Optional[datetime]
    data_exclusao_simples: Optional[datetime]
    opcao_mei: bool
    data_opcao_mei: Optional[datetime]
    data_exclusao_mei: Optional[datetime]
    empresa_cnpj: str


class SimplesNacionalCreate(SimplesNacionalBase):
    pass


class SimplesNacionalUpdate(SimplesNacionalBase):
    id: UUID
    opcao_simples: Optional[bool]
    opcao_mei: Optional[bool]
    empresa_cnpj: Optional[str]


class SimplesNacionalView(SimplesNacionalBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SimplesNacionalFilter(DefaultQueryFilter):
    opcao_simples: Optional[bool]
    data_opcao_simples: Optional[datetime]
    data_exclusao_simples: Optional[datetime]
    opcao_mei: Optional[bool]
    empresa_cnpj: Optional[str]
    data_opcao_mei: Optional[datetime]
    data_exclusao_mei: Optional[datetime]