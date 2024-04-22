#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps
from ..qualificacoes.schema import QualificacoesView
from ..base.schema import DefaultQueryFilter


class RepresentantesLegaisBase(BaseModel):
    cpf: str = Field(min_length=8, max_length=8)
    nome: str = Field(min_length=3)
    qualificacao_id: UUID


class RepresentantesLegaisCreate(RepresentantesLegaisBase):
    pass


class RepresentantesLegaisUpdate(RepresentantesLegaisBase):
    id: UUID
    cpf: Optional[str] = Field(min_length=8, max_length=8)
    nome: Optional[str] = Field(min_length=3)
    qualificacao_id: Optional[UUID]


class RepresentantesLegaisView(RepresentantesLegaisBase):
    id: UUID
    cpf: str
    nome: str
    # qualificacao: QualificacoesView
    created_at: datetime
    updated_at: datetime

    # def dict(self, **kwargs):
    #     kwargs['exclude'] = {'qualificacao_id'}
    #     return super().dict(**kwargs)

    # def json(self, **kwargs):
    #     kwargs['exclude'] = {'qualificacao_id'}
    #     return super().json(**kwargs)

    class Config:
        orm_mode = True


class RepresentantesLegaisFilter(DefaultQueryFilter):
    cpf: Optional[str]
    nome: Optional[str]
    qualificacao_id: Optional[UUID]
