#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from typing import Optional, List, Annotated
from datetime import datetime
from uuid import UUID

# ### Third-party deps
from pydantic import BaseModel, Field
from fastapi import Query

# ### Local deps
from ..portes_empresas.schema import PortesEmpresasView
from ..naturezas_juridicas.schema import NaturezasJuridicasView
from ..qualificacoes.schema import QualificacoesView
from ..simples_nacional.schema import SimplesNacionalView
from ..estabelecimentos.schema import EstabelecimentosView
from ..socios.schema import SociosView
from ..base.schema import DefaultQueryFilter


class EmpresasBase(BaseModel):
    cnpj_basico: str = Field(min_length=8, max_length=8)
    razao_social: str = Field(min_length=3)
    capital_social: float
    porte_empresa_id: UUID
    natureza_juridica_id: UUID
    qualificacao_responsavel_id: UUID


class EmpresasCreate(EmpresasBase):
    pass


class EmpresasUpdate(EmpresasBase):
    id: UUID
    cnpj_basico: Optional[str] = Field(min_length=8, max_length=8)
    razao_social: Optional[str] = Field(min_length=3)
    capital_social: Optional[float]
    porte_empresa_id: Optional[UUID]
    natureza_juridica_id: Optional[UUID]
    qualificacao_responsavel_id: Optional[UUID]


class EmpresasView(EmpresasBase):
    id: UUID
    cnpj_basico: str
    razao_social: str
    # porte_empresa: PortesEmpresasView
    # natureza_juridica: NaturezasJuridicasView
    # qualificacao_responsavel: QualificacoesView
    # simples_nacional: SimplesNacionalView
    # estabelecimentos: List[EstabelecimentosView]
    # socios: List[SociosView]
    created_at: datetime
    updated_at: datetime

    # def dict(self, **kwargs):
    #     kwargs['exclude'] = {'porte_empresa_id', 'natureza_juridica_id', 'qualificacao_responsavel_id'}
    #     return super().dict(**kwargs)

    # def json(self, **kwargs):
    #     kwargs['exclude'] = {'porte_empresa_id', 'natureza_juridica_id', 'qualificacao_responsavel_id'}
    #     return super().json(**kwargs)

    class Config:
        orm_mode = True


class EmpresasMainView(BaseModel):
    id: UUID
    cnpj: str
    razao_social: str
    nome_fantasia: str
    capital_social: float
    natureza_juridica: str
    cnae: str
    cnaes_secundarios: str
    porte_empresa: str
    situacao_cadastral: str
    motivo: str
    qualificacao: str
    cep: str
    municipio: str
    # uf: str
    opcao_simples: bool
    data_opcao_simples: Optional[datetime]
    data_exclusao_simples: Optional[datetime]
    # opcao_mei: bool

    class Config:
        orm_mode = True



class EmpresasFilter(DefaultQueryFilter):
    cnpj_basico: Optional[str]
    razao_social: Optional[str]
    cnae_id: Annotated[Optional[List[str]], Query()]
    situacao_cadastral_id: Annotated[Optional[List[str]], Query()]
    natureza_juridica_id: Annotated[Optional[List[str]], Query()]
    porte_empresa_id: Annotated[Optional[List[str]], Query()]
    min_capital_social: Optional[float] = 0
    max_capital_social: Optional[float] = 0
    opcao_simples: Optional[bool] = False
    opcao_mei: Optional[bool] = False
