#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel

# ### Local deps
from ..empresas.schema import EmpresasView


class SimplesNacionalBase(BaseModel):
    opcao_simples: bool
    data_opcao_simples: Optional[datetime]
    data_exclusao_simples: Optional[datetime]
    opcao_mei: bool
    data_opcao_mei: Optional[datetime]
    data_exclusao_mei: Optional[datetime]
    empresa_id: UUID


class SimplesNacionalCreate(SimplesNacionalBase):
    pass


class SimplesNacionalUpdate(SimplesNacionalBase):
    id: UUID
    opcao_simples: Optional[bool]
    opcao_mei: Optional[bool]
    empresa_id: Optional[UUID]


class SimplesNacionalShow(SimplesNacionalBase):
    id: int
    empresa: EmpresasView
    created_at: datetime
    updated_at: datetime

    def dict(self, **kwargs):
        kwargs['exclude'] = {'empresa_id'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'empresa_id'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
