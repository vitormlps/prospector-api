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
from ..representantes_legais.schema import RepresentantesLegaisView
from ..paises.schema import PaisesView
from ..faixas_etarias.schema import FaixasEtariasView
from ..base.schema import DefaultQueryFilter


class SociosBase(BaseModel):
    nome: str = Field(min_length=3)
    cpf_cnpj: Optional[str] = Field(min_length=8, max_length=14)
    data_entrada_sociedade: datetime
    empresa_cnpj: str
    qualificacao_id: UUID
    representante_legal_id: UUID
    pais_id: UUID
    faixa_etaria_id: UUID


class SociosCreate(SociosBase):
    pass


class SociosUpdate(SociosBase):
    id: UUID
    nome: Optional[str] = Field(min_length=3)
    data_entrada_sociedade: Optional[datetime]
    empresa_cnpj: Optional[str]
    qualificacao_id: Optional[UUID]
    representante_legal_id: Optional[UUID]
    pais_id: Optional[UUID]
    faixa_etaria_id: Optional[UUID]


class SociosView(SociosBase):
    id: UUID
    nome: str
    cpf_cnpj: Optional[str]
    # qualificacao: QualificacoesView
    representante_legal_id: Optional[UUID]
    # representante_legal: RepresentantesLegaisView
    pais_id: Optional[UUID]
    # pais: PaisesView
    faixa_etaria_id: Optional[UUID]
    # faixa_etaria: FaixasEtariasView
    created_at: datetime
    updated_at: datetime

    # def dict(self, **kwargs):
    #     kwargs['exclude'] = {'qualificacao_id', 'representante_legal_id', 'pais_id', 'faixa_etaria_id'}
    #     return super().dict(**kwargs)

    # def json(self, **kwargs):
    #     kwargs['exclude'] = {'qualificacao_id', 'representante_legal_id', 'pais_id', 'faixa_etaria_id'}
    #     return super().json(**kwargs)

    class Config:
        orm_mode = True


class SociosFilter(DefaultQueryFilter):
    nome: Optional[str]
    cpf_cnpj: Optional[str]
    data_entrada_sociedade: Optional[datetime]
    empresa_cnpj: Optional[str]
    qualificacao_id: Optional[UUID]
    representante_legal_id: Optional[UUID]
    pais_id: Optional[UUID]
    faixa_etaria_id: Optional[UUID]