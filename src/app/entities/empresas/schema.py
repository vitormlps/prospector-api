#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field

# ### Local deps
from ..portes_empresas.schema import PortesEmpresasView
from ..naturezas_juridicas.schema import NaturezasJuridicasView
from ..qualificacoes.schema import QualificacoesView
from ..simples_nacional.schema import SimplesNacionalView
from ..estabelecimentos.schema import EstabelecimentosView
from ..socios.schema import SociosView


class EmpresasBase(BaseModel):
    cnpj_basico: str = Field(min_length=8, max_length=8)
    razao_social: str = Field(min_length=3)
    capital_social: float = Field(decimal_places=2)
    porte_empresa_id: UUID
    natureza_juridica_id: UUID
    qualificacao_responsavel_id: UUID
    simples_nacional_id: UUID


class EmpresasCreate(EmpresasBase):
    pass


class EmpresasUpdate(EmpresasBase):
    id: UUID
    cnpj_basico: Optional[str] = Field(min_length=8, max_length=8)
    razao_social: Optional[str] = Field(min_length=3)
    capital_social: Optional[float] = Field(decimal_places=2)
    porte_empresa_id: Optional[UUID]
    natureza_juridica_id: Optional[UUID]
    qualificacao_responsavel_id: Optional[UUID]
    simples_nacional_id: Optional[UUID]


class EmpresasView(EmpresasBase):
    id: UUID
    porte_empresa: PortesEmpresasView
    natureza_juridica: NaturezasJuridicasView
    qualificacao_responsavel: QualificacoesView
    simples_nacional: SimplesNacionalView
    estabelecimentos: List[EstabelecimentosView]
    socios: List[SociosView]
    created_at: datetime
    updated_at: datetime

    def dict(self, **kwargs):
        kwargs['exclude'] = {'porte_empresa_id', 'natureza_juridica_id', 'qualificacao_responsavel_id', 'simples_nacional_id'}
        return super().dict(**kwargs)

    def json(self, **kwargs):
        kwargs['exclude'] = {'porte_empresa_id', 'natureza_juridica_id', 'qualificacao_responsavel_id', 'simples_nacional_id'}
        return super().json(**kwargs)

    class Config:
        orm_mode = True
